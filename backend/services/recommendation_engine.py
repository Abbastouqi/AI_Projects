"""
Complete RAG-based recommendation engine
Combines vector search, filtering, and GPT-4 generation
"""
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from openai import OpenAI
from core.config import settings
from services.vector_store_service import VectorStoreService
from services.query_processor import QueryProcessor
from models.database import Laptop
import json

class RecommendationEngine:
    """RAG-based laptop recommendation engine"""
    
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.query_processor = QueryProcessor()
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def get_recommendations(
        self,
        user_query: str,
        db: Session,
        conversation_history: Optional[List[Dict]] = None,
        n_results: int = 3
    ) -> Dict[str, Any]:
        """
        Get personalized laptop recommendations using RAG
        
        Args:
            user_query: User's natural language query
            db: Database session
            conversation_history: Previous conversation for context
            n_results: Number of recommendations to return
            
        Returns:
            Dictionary with recommendations and explanation
        """
        try:
            # Step 1: Extract requirements from query
            requirements = self.query_processor.extract_requirements(
                user_query,
                conversation_history
            )
            
            # Step 2: Build optimized search query
            search_query = self.query_processor.build_search_query(requirements)
            
            # Step 3: Retrieve similar laptops from vector store
            vector_results = self.vector_store.search(
                query=search_query,
                n_results=10  # Get more for filtering
            )
            
            if not vector_results:
                return self._handle_no_results(user_query, requirements)
            
            # Step 4: Get full laptop details from database
            laptop_ids = [result['laptop_id'] for result in vector_results]
            laptops = db.query(Laptop).filter(Laptop.id.in_(laptop_ids)).all()
            
            # Create lookup for similarity scores
            similarity_scores = {
                result['laptop_id']: result['similarity_score']
                for result in vector_results
            }
            
            # Step 5: Filter by requirements
            filtered_laptops = self._filter_laptops(
                laptops,
                requirements,
                similarity_scores
            )
            
            if not filtered_laptops:
                return self._handle_no_results(user_query, requirements)
            
            # Step 6: Rank and select top N
            top_laptops = filtered_laptops[:n_results]
            
            # Step 7: Generate personalized recommendations with GPT-4
            recommendations = self._generate_recommendations(
                top_laptops,
                requirements,
                user_query,
                conversation_history
            )
            
            return {
                "success": True,
                "recommendations": recommendations,
                "requirements_extracted": requirements,
                "search_query_used": search_query
            }
            
        except Exception as e:
            print(f"Error in recommendation engine: {e}")
            return {
                "success": False,
                "error": str(e),
                "recommendations": []
            }
    
    def _filter_laptops(
        self,
        laptops: List[Laptop],
        requirements: Dict[str, Any],
        similarity_scores: Dict[int, float]
    ) -> List[Tuple[Laptop, float, float]]:
        """
        Filter and score laptops based on requirements
        
        Returns:
            List of (laptop, similarity_score, requirement_score) tuples
        """
        scored_laptops = []
        
        for laptop in laptops:
            # Get similarity score
            similarity = similarity_scores.get(laptop.id, 0.0)
            
            # Calculate requirement match score
            req_score = self._calculate_requirement_score(laptop, requirements)
            
            # Budget filter (hard constraint)
            if requirements.get('budget'):
                budget = requirements['budget']
                if budget.get('min') and laptop.price_pkr < budget['min']:
                    continue
                if budget.get('max') and laptop.price_pkr > budget['max']:
                    continue
            
            # Combined score (weighted)
            combined_score = (similarity * 0.6) + (req_score * 0.4)
            
            scored_laptops.append((laptop, similarity, combined_score))
        
        # Sort by combined score
        scored_laptops.sort(key=lambda x: x[2], reverse=True)
        
        return scored_laptops
    
    def _calculate_requirement_score(
        self,
        laptop: Laptop,
        requirements: Dict[str, Any]
    ) -> float:
        """Calculate how well laptop matches requirements (0-1)"""
        score = 0.0
        total_weight = 0.0
        
        # Use case match (weight: 0.4)
        if requirements.get('use_case'):
            use_cases = requirements['use_case']
            if isinstance(use_cases, str):
                use_cases = [use_cases]
            
            # Map use cases to ideal_for categories
            use_case_mapping = {
                "programming": ["Programming", "CS Student", "Software Development"],
                "gaming": ["Gaming"],
                "studies": ["FSC Student", "CS Student", "Office Work"],
                "engineering": ["Engineering"],
                "data_science": ["Data Science", "Machine Learning"],
                "video_editing": ["Video Editing", "Content Creation"],
                "graphic_design": ["Graphic Design"],
                "office_work": ["Office Work", "Business"]
            }
            
            match_count = 0
            for use_case in use_cases:
                mapped_categories = use_case_mapping.get(use_case, [])
                for category in mapped_categories:
                    if category in laptop.ideal_for:
                        match_count += 1
                        break
            
            if use_cases:
                score += (match_count / len(use_cases)) * 0.4
            total_weight += 0.4
        
        # Brand preference (weight: 0.2)
        if requirements.get('brand_preference'):
            if laptop.brand == requirements['brand_preference']:
                score += 0.2
            total_weight += 0.2
        
        # RAM preference (weight: 0.2)
        if requirements.get('ram_preference'):
            if laptop.ram_gb >= requirements['ram_preference']:
                score += 0.2
            elif laptop.ram_gb >= requirements['ram_preference'] * 0.75:
                score += 0.1
            total_weight += 0.2
        
        # Storage preference (weight: 0.2)
        if requirements.get('storage_preference'):
            storage_pref = requirements['storage_preference']
            
            if storage_pref.get('type'):
                if laptop.storage_type == storage_pref['type']:
                    score += 0.1
            
            if storage_pref.get('size_gb'):
                if laptop.storage_gb >= storage_pref['size_gb']:
                    score += 0.1
            
            total_weight += 0.2
        
        # Normalize score
        if total_weight > 0:
            return score / total_weight
        
        return 0.5  # Default neutral score
    
    def _generate_recommendations(
        self,
        laptops: List[Tuple[Laptop, float, float]],
        requirements: Dict[str, Any],
        user_query: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> List[Dict[str, Any]]:
        """Generate personalized recommendations with GPT-4"""
        
        # Prepare laptop data for GPT
        laptops_data = []
        for rank, (laptop, similarity, score) in enumerate(laptops, 1):
            laptops_data.append({
                "rank": rank,
                "id": laptop.id,
                "brand": laptop.brand,
                "model": laptop.model,
                "cpu": laptop.cpu,
                "ram_gb": laptop.ram_gb,
                "storage": f"{laptop.storage_gb}GB {laptop.storage_type}",
                "gpu": laptop.gpu,
                "display_size": laptop.display_size,
                "price_pkr": laptop.price_pkr,
                "battery_hours": laptop.battery_hours,
                "weight_kg": laptop.weight_kg,
                "ideal_for": laptop.ideal_for,
                "similarity_score": round(similarity, 3)
            })
        
        # Build GPT prompt
        system_prompt = """You are an expert laptop advisor for Pakistani students and professionals.
Your task is to explain why each laptop is recommended based on the user's needs.

For each laptop, provide:
1. A personalized reason (2-3 sentences) explaining why it's suitable
2. Key strengths specific to their use case
3. Any considerations they should know

Be conversational, helpful, and specific. Mention Pakistani context (prices in PKR, local availability).
Focus on value for money and practical benefits."""
        
        user_prompt = f"""User Query: {user_query}

Extracted Requirements:
{json.dumps(requirements, indent=2)}

Top Recommended Laptops:
{json.dumps(laptops_data, indent=2)}

Please provide personalized recommendations for each laptop. Return a JSON array with this structure:
[
  {{
    "laptop_id": 1,
    "rank": 1,
    "reason": "Detailed explanation why this laptop is perfect for them",
    "key_strengths": ["Strength 1", "Strength 2", "Strength 3"],
    "considerations": "Any important notes or considerations"
  }}
]"""
        
        try:
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation context
            if conversation_history:
                for msg in conversation_history[-3:]:
                    messages.append(msg)
            
            messages.append({"role": "user", "content": user_prompt})
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )
            
            result = response.choices[0].message.content.strip()
            
            # Parse JSON response
            if result.startswith('```json'):
                result = result.split('```json')[1].split('```')[0].strip()
            elif result.startswith('```'):
                result = result.split('```')[1].split('```')[0].strip()
            
            gpt_recommendations = json.loads(result)
            
            # Merge with laptop data
            final_recommendations = []
            for gpt_rec in gpt_recommendations:
                laptop_id = gpt_rec['laptop_id']
                
                # Find matching laptop
                laptop_data = next(
                    (l for l in laptops_data if l['id'] == laptop_id),
                    None
                )
                
                if laptop_data:
                    final_recommendations.append({
                        **laptop_data,
                        "reason": gpt_rec.get('reason', ''),
                        "key_strengths": gpt_rec.get('key_strengths', []),
                        "considerations": gpt_rec.get('considerations', '')
                    })
            
            return final_recommendations
            
        except Exception as e:
            print(f"Error generating GPT recommendations: {e}")
            
            # Fallback: return basic recommendations
            return [
                {
                    **laptop_data,
                    "reason": f"This {laptop_data['brand']} {laptop_data['model']} matches your requirements with {laptop_data['ram_gb']}GB RAM and {laptop_data['storage']} at PKR {laptop_data['price_pkr']:,}.",
                    "key_strengths": laptop_data['ideal_for'],
                    "considerations": "Check local availability and warranty."
                }
                for laptop_data in laptops_data
            ]
    
    def _handle_no_results(
        self,
        user_query: str,
        requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle case when no laptops match requirements"""
        
        suggestions = []
        
        if requirements.get('budget'):
            budget = requirements['budget']
            if budget.get('max') and budget['max'] < 70000:
                suggestions.append("Consider increasing your budget to at least PKR 70,000 for better options.")
            elif budget.get('min') and budget['min'] > 250000:
                suggestions.append("Your budget is quite high. Consider premium brands or gaming laptops.")
        
        if requirements.get('brand_preference'):
            suggestions.append(f"Try removing the {requirements['brand_preference']} brand filter to see more options.")
        
        return {
            "success": False,
            "message": "No laptops found matching your exact requirements.",
            "suggestions": suggestions,
            "requirements_extracted": requirements,
            "recommendations": []
        }
