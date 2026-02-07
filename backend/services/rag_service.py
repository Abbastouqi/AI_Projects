"""
Enhanced RAG service using the complete recommendation engine
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from services.recommendation_engine import RecommendationEngine
from services.query_processor import QueryProcessor
from openai import OpenAI
from core.config import settings

class RAGService:
    """Main service for RAG-based laptop recommendations"""
    
    def __init__(self):
        self.recommendation_engine = RecommendationEngine()
        self.query_processor = QueryProcessor()
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.sessions = {}
    
    async def get_recommendation(
        self,
        query: str,
        session_id: str,
        db: Session
    ) -> tuple[str, List[Dict[str, Any]]]:
        """
        Get laptop recommendations with conversational response
        
        Args:
            query: User's message
            session_id: Session identifier
            db: Database session
            
        Returns:
            Tuple of (response_text, recommendations_list)
        """
        # Get or create conversation history
        conversation_history = self._get_conversation_history(session_id)
        
        # Add user message to history
        conversation_history.append({
            "role": "user",
            "content": query
        })
        
        # Check if user is asking for recommendations or just chatting
        needs_recommendation = self._needs_recommendation(query, conversation_history)
        
        if needs_recommendation:
            # Get recommendations using RAG engine
            result = self.recommendation_engine.get_recommendations(
                user_query=query,
                db=db,
                conversation_history=conversation_history,
                n_results=3
            )
            
            if result['success']:
                # Generate conversational response
                response_text = self._generate_conversational_response(
                    query=query,
                    recommendations=result['recommendations'],
                    requirements=result.get('requirements_extracted', {}),
                    conversation_history=conversation_history
                )
                
                # Update conversation history
                conversation_history.append({
                    "role": "assistant",
                    "content": response_text
                })
                self.sessions[session_id] = conversation_history
                
                return response_text, result['recommendations']
            else:
                # No results found
                response_text = result.get('message', 'Sorry, I could not find suitable laptops.')
                if result.get('suggestions'):
                    response_text += "\n\n" + "\n".join(result['suggestions'])
                
                conversation_history.append({
                    "role": "assistant",
                    "content": response_text
                })
                self.sessions[session_id] = conversation_history
                
                return response_text, []
        else:
            # Just conversational response
            response_text = self._generate_chat_response(query, conversation_history)
            
            conversation_history.append({
                "role": "assistant",
                "content": response_text
            })
            self.sessions[session_id] = conversation_history
            
            return response_text, []
    
    def _get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get or initialize conversation history"""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]
    
    def _needs_recommendation(self, query: str, history: List[Dict]) -> bool:
        """Determine if user is asking for recommendations"""
        query_lower = query.lower()
        
        # Keywords indicating recommendation request
        recommendation_keywords = [
            'recommend', 'suggest', 'need', 'want', 'looking for',
            'budget', 'price', 'laptop', 'buy', 'purchase',
            'programming', 'gaming', 'student', 'fsc'
        ]
        
        # Check if query contains recommendation keywords
        for keyword in recommendation_keywords:
            if keyword in query_lower:
                return True
        
        # If conversation is new or short, likely asking for recommendations
        if len(history) <= 2:
            return True
        
        return False
    
    def _generate_conversational_response(
        self,
        query: str,
        recommendations: List[Dict],
        requirements: Dict,
        conversation_history: List[Dict]
    ) -> str:
        """Generate natural conversational response with recommendations"""
        
        if not recommendations:
            return "I couldn't find any laptops matching your requirements. Could you adjust your budget or requirements?"
        
        # Build response
        response_parts = []
        
        # Acknowledge requirements
        if requirements.get('budget'):
            budget = requirements['budget']
            response_parts.append(
                f"Based on your budget of PKR {budget.get('min', 0):,} - {budget.get('max', 0):,}, "
            )
        
        if requirements.get('use_case'):
            use_cases = requirements['use_case']
            if isinstance(use_cases, list):
                use_case_str = ' and '.join(use_cases)
            else:
                use_case_str = use_cases
            response_parts.append(f"for {use_case_str}, ")
        
        response_parts.append(f"I found {len(recommendations)} great options for you:\n\n")
        
        # Add recommendations
        for i, rec in enumerate(recommendations, 1):
            response_parts.append(
                f"**{i}. {rec['brand']} {rec['model']}** - PKR {rec['price_pkr']:,}\n"
            )
            response_parts.append(f"{rec.get('reason', '')}\n\n")
        
        response_parts.append(
            "Would you like more details about any of these laptops, or should I adjust the recommendations?"
        )
        
        return "".join(response_parts)
    
    def _generate_chat_response(
        self,
        query: str,
        conversation_history: List[Dict]
    ) -> str:
        """Generate conversational response for non-recommendation queries"""
        
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are a friendly laptop recommendation assistant for Pakistani students.
Help users find the perfect laptop by asking about:
- Their field of study or work (FSC, programming, engineering, etc.)
- Budget in Pakistani Rupees (PKR)
- Specific requirements (RAM, storage, brand preference)

Be conversational and helpful. Guide them towards providing enough information for recommendations."""
                }
            ]
            
            # Add conversation history
            messages.extend(conversation_history[-5:])  # Last 5 messages
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.8,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating chat response: {e}")
            return "I'm here to help you find the perfect laptop! Could you tell me about your budget and what you'll be using the laptop for?"
