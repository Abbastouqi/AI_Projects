"""
Query processor to extract user requirements from natural language
"""
from typing import Dict, Optional, List, Any
import re
from openai import OpenAI
from core.config import settings
import json

class QueryProcessor:
    """Extract structured information from user queries"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Keywords for different categories
        self.use_case_keywords = {
            "programming": ["programming", "coding", "developer", "software", "python", "java", "web development", "app development"],
            "gaming": ["gaming", "games", "gamer", "play games", "fortnite", "valorant", "pubg"],
            "studies": ["study", "student", "fsc", "college", "university", "classes", "assignments", "notes"],
            "engineering": ["engineering", "cad", "autocad", "solidworks", "simulation", "technical"],
            "data_science": ["data science", "machine learning", "ml", "ai", "data analysis", "jupyter"],
            "video_editing": ["video editing", "premiere", "after effects", "content creation", "youtube"],
            "graphic_design": ["graphic design", "photoshop", "illustrator", "design work"],
            "office_work": ["office", "excel", "word", "powerpoint", "business", "work from home"]
        }
        
        self.brand_keywords = {
            "HP": ["hp", "hewlett packard"],
            "Dell": ["dell"],
            "Lenovo": ["lenovo"],
            "ASUS": ["asus"],
            "Acer": ["acer"],
            "MSI": ["msi"],
            "Apple": ["apple", "macbook"]
        }
    
    def extract_requirements(self, query: str, conversation_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Extract structured requirements from user query
        
        Args:
            query: User's message
            conversation_history: Previous conversation for context
            
        Returns:
            Dictionary with extracted requirements
        """
        query_lower = query.lower()
        
        # Extract budget
        budget = self._extract_budget(query)
        
        # Extract use case
        use_case = self._extract_use_case(query_lower)
        
        # Extract brand preference
        brand_preference = self._extract_brand(query_lower)
        
        # Extract RAM preference
        ram_preference = self._extract_ram(query_lower)
        
        # Extract storage preference
        storage_preference = self._extract_storage(query_lower)
        
        # Use GPT for more nuanced extraction if needed
        if not use_case or not budget:
            gpt_extracted = self._extract_with_gpt(query, conversation_history)
            
            if not budget and gpt_extracted.get('budget'):
                budget = gpt_extracted['budget']
            
            if not use_case and gpt_extracted.get('use_case'):
                use_case = gpt_extracted['use_case']
        
        return {
            "budget": budget,
            "use_case": use_case,
            "brand_preference": brand_preference,
            "ram_preference": ram_preference,
            "storage_preference": storage_preference,
            "original_query": query
        }
    
    def _extract_budget(self, query: str) -> Optional[Dict[str, int]]:
        """Extract budget from query"""
        # Look for patterns like "100000", "1 lakh", "under 150000", "between 80000 and 120000"
        
        # Pattern: "under X" or "below X" or "max X"
        under_match = re.search(r'(?:under|below|max|maximum|upto|up to)\s*(?:pkr|rs)?\s*(\d+(?:,\d+)*(?:k|lakh)?)', query.lower())
        if under_match:
            amount = self._parse_amount(under_match.group(1))
            return {"min": 0, "max": amount}
        
        # Pattern: "above X" or "over X" or "min X"
        above_match = re.search(r'(?:above|over|min|minimum|at least)\s*(?:pkr|rs)?\s*(\d+(?:,\d+)*(?:k|lakh)?)', query.lower())
        if above_match:
            amount = self._parse_amount(above_match.group(1))
            return {"min": amount, "max": 500000}
        
        # Pattern: "between X and Y"
        between_match = re.search(r'between\s*(?:pkr|rs)?\s*(\d+(?:,\d+)*(?:k|lakh)?)\s*(?:and|to|-)\s*(?:pkr|rs)?\s*(\d+(?:,\d+)*(?:k|lakh)?)', query.lower())
        if between_match:
            min_amount = self._parse_amount(between_match.group(1))
            max_amount = self._parse_amount(between_match.group(2))
            return {"min": min_amount, "max": max_amount}
        
        # Pattern: just a number with PKR/Rs
        amount_match = re.search(r'(?:pkr|rs|rupees)\s*(\d+(?:,\d+)*(?:k|lakh)?)', query.lower())
        if amount_match:
            amount = self._parse_amount(amount_match.group(1))
            # Assume +/- 20% range
            return {"min": int(amount * 0.8), "max": int(amount * 1.2)}
        
        # Pattern: standalone number that looks like a price
        standalone_match = re.search(r'\b(\d{5,6})\b', query)
        if standalone_match:
            amount = int(standalone_match.group(1))
            if 50000 <= amount <= 500000:  # Reasonable laptop price range
                return {"min": int(amount * 0.8), "max": int(amount * 1.2)}
        
        return None
    
    def _parse_amount(self, amount_str: str) -> int:
        """Parse amount string to integer"""
        amount_str = amount_str.lower().replace(',', '')
        
        if 'lakh' in amount_str:
            num = float(re.search(r'[\d.]+', amount_str).group())
            return int(num * 100000)
        elif 'k' in amount_str:
            num = float(re.search(r'[\d.]+', amount_str).group())
            return int(num * 1000)
        else:
            return int(re.search(r'\d+', amount_str).group())
    
    def _extract_use_case(self, query_lower: str) -> Optional[List[str]]:
        """Extract use case from query"""
        detected_cases = []
        
        for use_case, keywords in self.use_case_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    detected_cases.append(use_case)
                    break
        
        return detected_cases if detected_cases else None
    
    def _extract_brand(self, query_lower: str) -> Optional[str]:
        """Extract brand preference"""
        for brand, keywords in self.brand_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return brand
        return None
    
    def _extract_ram(self, query_lower: str) -> Optional[int]:
        """Extract RAM requirement"""
        ram_match = re.search(r'(\d+)\s*gb\s*ram', query_lower)
        if ram_match:
            return int(ram_match.group(1))
        
        if '16gb' in query_lower or '16 gb' in query_lower:
            return 16
        elif '8gb' in query_lower or '8 gb' in query_lower:
            return 8
        
        return None
    
    def _extract_storage(self, query_lower: str) -> Optional[Dict[str, Any]]:
        """Extract storage requirements"""
        storage = {}
        
        # Storage size
        storage_match = re.search(r'(\d+)\s*gb\s*(?:ssd|storage)', query_lower)
        if storage_match:
            storage['size_gb'] = int(storage_match.group(1))
        
        # Storage type
        if 'ssd' in query_lower:
            storage['type'] = 'SSD'
        elif 'hdd' in query_lower:
            storage['type'] = 'HDD'
        
        return storage if storage else None
    
    def _extract_with_gpt(self, query: str, conversation_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Use GPT to extract requirements when regex fails"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are a requirement extractor for a laptop recommendation system.
Extract the following from user messages:
1. Budget (in PKR) - return as {"min": X, "max": Y}
2. Use case - one or more of: programming, gaming, studies, engineering, data_science, video_editing, graphic_design, office_work
3. Brand preference - HP, Dell, Lenovo, ASUS, etc.

Return ONLY a JSON object with these fields. If something is not mentioned, use null.
Example: {"budget": {"min": 80000, "max": 120000}, "use_case": ["programming", "studies"], "brand_preference": "HP"}"""
                }
            ]
            
            # Add conversation history for context
            if conversation_history:
                for msg in conversation_history[-3:]:  # Last 3 messages
                    messages.append(msg)
            
            messages.append({"role": "user", "content": query})
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.3,
                max_tokens=200
            )
            
            result = response.choices[0].message.content.strip()
            
            # Try to parse JSON
            if result.startswith('```json'):
                result = result.split('```json')[1].split('```')[0].strip()
            elif result.startswith('```'):
                result = result.split('```')[1].split('```')[0].strip()
            
            extracted = json.loads(result)
            return extracted
            
        except Exception as e:
            print(f"Error extracting with GPT: {e}")
            return {}
    
    def build_search_query(self, requirements: Dict[str, Any]) -> str:
        """
        Build optimized search query for vector store
        
        Args:
            requirements: Extracted requirements
            
        Returns:
            Optimized search query string
        """
        query_parts = []
        
        # Add use case
        if requirements.get('use_case'):
            use_cases = requirements['use_case']
            if isinstance(use_cases, list):
                query_parts.append(f"Laptop for {' and '.join(use_cases)}")
            else:
                query_parts.append(f"Laptop for {use_cases}")
        
        # Add budget context
        if requirements.get('budget'):
            budget = requirements['budget']
            if budget.get('max'):
                if budget['max'] < 90000:
                    query_parts.append("budget-friendly affordable")
                elif budget['max'] < 150000:
                    query_parts.append("mid-range good value")
                else:
                    query_parts.append("premium high-end")
        
        # Add brand
        if requirements.get('brand_preference'):
            query_parts.append(f"{requirements['brand_preference']} brand")
        
        # Add RAM
        if requirements.get('ram_preference'):
            query_parts.append(f"{requirements['ram_preference']}GB RAM")
        
        # Add storage
        if requirements.get('storage_preference'):
            storage = requirements['storage_preference']
            if storage.get('type'):
                query_parts.append(f"{storage['type']} storage")
        
        # Fallback to original query
        if not query_parts and requirements.get('original_query'):
            return requirements['original_query']
        
        return " ".join(query_parts)
