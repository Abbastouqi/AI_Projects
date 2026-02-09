"""
Conversation Flow Manager for Laptop Recommendation Chatbot
Handles intent detection, state management, and response generation
"""
from typing import Dict, List, Optional, Tuple
from enum import Enum
import re
from datetime import datetime
from sqlalchemy.orm import Session
from models.database import UserSession
from services.laptop_service import LaptopService

class Intent(Enum):
    GREETING = "greeting"
    BUDGET_QUERY = "budget_query"
    USE_CASE_QUERY = "use_case_query"
    COMPARISON_REQUEST = "comparison_request"
    SPECIFIC_LAPTOP = "specific_laptop_question"
    PURCHASE_HELP = "purchase_help"
    UNKNOWN = "unknown"

class ConversationStep(Enum):
    GREETING = "greeting"
    NEEDS_ANALYSIS = "needs_analysis"
    BUDGET_CHECK = "budget_check"
    RECOMMENDATION = "recommendation"
    COMPARISON = "comparison"
    PURCHASE_GUIDANCE = "purchase_guidance"

class UserProfile:
    def __init__(self):
        self.student_type: Optional[str] = None  # FSC, Uni
        self.major: Optional[str] = None  # CS, Engineering, Medical, etc.
        self.use_case: List[str] = []  # Programming, Gaming, Office, etc.
        self.budget_min: Optional[int] = None
        self.budget_max: Optional[int] = None
        self.brand_pref: List[str] = []
        self.ram_pref: Optional[int] = None
        self.storage_pref: Optional[str] = None
        
    def to_dict(self) -> Dict:
        return {
            "student_type": self.student_type,
            "major": self.major,
            "use_case": self.use_case,
            "budget_min": self.budget_min,
            "budget_max": self.budget_max,
            "brand_pref": self.brand_pref,
            "ram_pref": self.ram_pref,
            "storage_pref": self.storage_pref
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        profile = cls()
        profile.student_type = data.get("student_type")
        profile.major = data.get("major")
        profile.use_case = data.get("use_case", [])
        profile.budget_min = data.get("budget_min")
        profile.budget_max = data.get("budget_max")
        profile.brand_pref = data.get("brand_pref", [])
        profile.ram_pref = data.get("ram_pref")
        profile.storage_pref = data.get("storage_pref")
        return profile

class ConversationFlowManager:
    """Manages conversation flow and generates contextual responses"""
    
    def __init__(self, db: Session):
        self.db = db
        self.laptop_service = LaptopService()
        
        # Intent detection patterns
        self.intent_patterns = {
            Intent.GREETING: [
                r'\b(hi|hello|hey|salam|assalam|greetings)\b',
                r'\b(good morning|good evening)\b'
            ],
            Intent.BUDGET_QUERY: [
                r'\b(\d+k?)\s*(to|se|tak)\s*(\d+k?)\b',
                r'\bbudget\b.*\b(\d+)\b',
                r'\b(\d{5,6})\s*(rupees|pkr|rs)\b',
                r'\b(cheap|affordable|budget|economical)\b'
            ],
            Intent.USE_CASE_QUERY: [
                r'\b(programming|coding|development|software)\b',
                r'\b(fsc|pre-engineering|pre-medical|ics)\b',
                r'\b(gaming|games|pubg|gta)\b',
                r'\b(video editing|editing|premiere|photoshop)\b',
                r'\b(office work|ms office|excel|word)\b',
                r'\b(student|study|university|college)\b'
            ],
            Intent.COMPARISON_REQUEST: [
                r'\b(compare|comparison|vs|versus|difference)\b',
                r'\b(which is better|better than)\b',
                r'\b(hp vs dell|lenovo vs asus)\b'
            ],
            Intent.SPECIFIC_LAPTOP: [
                r'\b(hp|dell|lenovo|asus|acer|msi)\s+\w+',
                r'\b(i3|i5|i7|ryzen)\b',
                r'\b(inspiron|pavilion|ideapad|vivobook)\b'
            ],
            Intent.PURCHASE_HELP: [
                r'\b(where to buy|kahan se|purchase|order)\b',
                r'\b(czone|paklap|daraz|telemart)\b',
                r'\b(reliable|trusted|authentic)\b',
                r'\b(warranty|guarantee)\b'
            ]
        }
    
    def detect_intent(self, message: str) -> Intent:
        """Detect user intent from message"""
        message_lower = message.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        return Intent.UNKNOWN
    
    def extract_budget(self, message: str) -> Tuple[Optional[int], Optional[int]]:
        """Extract budget range from message"""
        message_lower = message.lower()
        
        # Pattern: "80k to 120k" or "80000 to 120000"
        range_match = re.search(r'(\d+)k?\s*(to|se|tak|-)\s*(\d+)k?', message_lower)
        if range_match:
            min_val = int(range_match.group(1))
            max_val = int(range_match.group(3))
            # Convert k to thousands
            if min_val < 1000:
                min_val *= 1000
            if max_val < 1000:
                max_val *= 1000
            return min_val, max_val
        
        # Pattern: single budget "around 100k" or "100000"
        single_match = re.search(r'(\d+)k?\s*(rupees|pkr|rs)?', message_lower)
        if single_match:
            budget = int(single_match.group(1))
            if budget < 1000:
                budget *= 1000
            # Create range ±20%
            return int(budget * 0.8), int(budget * 1.2)
        
        return None, None
    
    def extract_use_cases(self, message: str) -> List[str]:
        """Extract use cases from message"""
        message_lower = message.lower()
        use_cases = []
        
        use_case_keywords = {
            "Programming": ["programming", "coding", "development", "software", "cs", "computer science"],
            "FSC Student": ["fsc", "pre-engineering", "pre-medical", "intermediate"],
            "Gaming": ["gaming", "games", "pubg", "gta", "valorant"],
            "Video Editing": ["video editing", "editing", "premiere", "photoshop", "content creation"],
            "Office Work": ["office", "ms office", "excel", "word", "business"],
            "Engineering": ["engineering", "autocad", "solidworks", "matlab"],
            "Graphic Design": ["graphic design", "design", "illustrator", "photoshop"]
        }
        
        for use_case, keywords in use_case_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                use_cases.append(use_case)
        
        return use_cases
    
    def extract_brands(self, message: str) -> List[str]:
        """Extract brand preferences"""
        message_lower = message.lower()
        brands = []
        
        brand_list = ["HP", "Dell", "Lenovo", "ASUS", "Acer", "MSI", "Apple"]
        for brand in brand_list:
            if brand.lower() in message_lower:
                brands.append(brand)
        
        return brands
    
    def get_current_step(self, session_id: str) -> ConversationStep:
        """Get current conversation step from session"""
        session = self.db.query(UserSession).filter(
            UserSession.session_id == session_id
        ).first()
        
        if not session or not session.preferences:
            return ConversationStep.GREETING
        
        prefs = session.preferences
        
        # Determine step based on collected info
        if not prefs.get("greeted"):
            return ConversationStep.GREETING
        elif not prefs.get("use_case"):
            return ConversationStep.NEEDS_ANALYSIS
        elif not prefs.get("budget_max"):
            return ConversationStep.BUDGET_CHECK
        elif prefs.get("recommendations_shown"):
            return ConversationStep.COMPARISON
        else:
            return ConversationStep.RECOMMENDATION
    
    def update_profile(self, session_id: str, message: str) -> UserProfile:
        """Update user profile based on message"""
        session = self.db.query(UserSession).filter(
            UserSession.session_id == session_id
        ).first()
        
        if not session:
            session = UserSession(
                session_id=session_id,
                conversation_history=[],
                preferences={}
            )
            self.db.add(session)
        
        # Load existing profile
        profile = UserProfile.from_dict(session.preferences)
        
        # Extract information
        budget_min, budget_max = self.extract_budget(message)
        if budget_min:
            profile.budget_min = budget_min
            profile.budget_max = budget_max
        
        use_cases = self.extract_use_cases(message)
        if use_cases:
            profile.use_case.extend([uc for uc in use_cases if uc not in profile.use_case])
        
        brands = self.extract_brands(message)
        if brands:
            profile.brand_pref.extend([b for b in brands if b not in profile.brand_pref])
        
        # Detect student type
        message_lower = message.lower()
        if "fsc" in message_lower or "intermediate" in message_lower:
            profile.student_type = "FSC"
        elif "university" in message_lower or "uni" in message_lower:
            profile.student_type = "Uni"
        
        # Detect major
        if any(word in message_lower for word in ["cs", "computer science", "software"]):
            profile.major = "CS"
        elif "engineering" in message_lower:
            profile.major = "Engineering"
        elif "medical" in message_lower or "mbbs" in message_lower:
            profile.major = "Medical"
        
        # Save profile
        session.preferences = profile.to_dict()
        self.db.commit()
        
        return profile
    
    def handle_greeting(self, session_id: str) -> str:
        """Handle greeting intent"""
        session = self.db.query(UserSession).filter(
            UserSession.session_id == session_id
        ).first()
        
        if session and session.preferences.get("greeted"):
            return "Welcome back! How can I help you find the perfect laptop today?"
        
        # Mark as greeted
        if session:
            session.preferences["greeted"] = True
            self.db.commit()
        
        return """السلام علیکم! Welcome to Pakistan's smartest laptop recommendation assistant! 🎓💻

I'm here to help Pakistani students find the perfect laptop within their budget. I know the local market (Czone, Paklap, Daraz) and can recommend based on your needs.

To get started, tell me:
1. What will you use the laptop for? (FSC studies, programming, gaming, etc.)
2. What's your budget in PKR?

Let's find your ideal laptop! 🚀"""
    
    def handle_budget_query(self, session_id: str, message: str, profile: UserProfile) -> str:
        """Handle budget-related queries"""
        if not profile.budget_max:
            return """I'd love to help! What's your budget range in PKR?

For example:
• "80k to 120k"
• "Around 100,000 rupees"
• "Maximum 150k"

Pakistani laptop prices typically range from 60k (basic) to 250k+ (premium)."""
        
        # Budget is set, provide guidance
        if profile.budget_max < 80000:
            return f"""With a budget of PKR {profile.budget_min:,} - {profile.budget_max:,}, I recommend considering:

💡 **Smart Options:**
1. **Refurbished/Used laptops** from trusted sellers (Czone, Paklap)
   - Can get better specs for same price
   - Look for 6-month warranty minimum

2. **Entry-level new laptops:**
   - HP 15s series (i3, 8GB RAM) ~75-85k
   - Lenovo V15 (Ryzen 3, 8GB) ~70-80k

3. **Payment plans** from Daraz/Telemart
   - 0% installments available

Would you like specific recommendations in this range?"""
        
        elif profile.budget_max < 120000:
            return f"""Great! PKR {profile.budget_min:,} - {profile.budget_max:,} is a solid mid-range budget.

You can get:
✅ Intel i5 or Ryzen 5 processor
✅ 8GB RAM (upgradeable)
✅ 512GB SSD
✅ Good for programming, office work, light gaming

Popular choices:
• HP 15s-fq5327tu (~115k)
• Lenovo IdeaPad 3 (~108k)
• Dell Inspiron 15 3530 (~125k)

What will you primarily use the laptop for?"""
        
        else:
            return f"""Excellent budget of PKR {profile.budget_min:,} - {profile.budget_max:,}! 

You can get premium features:
✅ Intel i7 or Ryzen 7
✅ 16GB RAM
✅ 512GB+ SSD
✅ Dedicated GPU options
✅ Perfect for heavy programming, video editing, gaming

Tell me your use case and I'll recommend the best options!"""
    
    def handle_use_case_query(self, session_id: str, message: str, profile: UserProfile) -> str:
        """Handle use case queries"""
        if not profile.use_case:
            return """What will you use the laptop for? Select all that apply:

📚 FSC/Intermediate student (notes, assignments)
💻 Programming/Software Development
🎮 Gaming
🎬 Video Editing
📊 Office Work (Excel, Word, PowerPoint)
🔧 Engineering (CAD, MATLAB)
🎨 Graphic Design

Just tell me your needs and I'll recommend accordingly!"""
        
        # Generate recommendations based on use case
        recommendations = []
        
        if "Programming" in profile.use_case or profile.major == "CS":
            recommendations.append("""
**For Programming:**
✅ Minimum: Intel i5/Ryzen 5 (10th gen+)
✅ RAM: 8GB minimum, 16GB recommended
✅ SSD: 512GB for fast compilation
✅ Good keyboard and battery life

Why? IDEs like VS Code, Android Studio need good RAM and processor.""")
        
        if "FSC Student" in profile.use_case or profile.student_type == "FSC":
            recommendations.append("""
**For FSC Pre-Engineering:**
✅ Intel i3/Ryzen 3 is sufficient
✅ 8GB RAM for multitasking
✅ 256-512GB SSD
✅ Good battery life (6+ hours)

You don't need high specs for notes, PDFs, and online classes.""")
        
        if "Gaming" in profile.use_case:
            recommendations.append("""
**For Gaming:**
⚠️ Budget gaming laptops start at 150k+
✅ Dedicated GPU (GTX 1650 minimum)
✅ Intel i5/Ryzen 5 (H-series)
✅ 16GB RAM
✅ Good cooling system

Note: Most laptops under 120k have integrated graphics (light gaming only).""")
        
        response = "\n".join(recommendations)
        
        if profile.budget_max:
            response += f"\n\nBased on your budget of PKR {profile.budget_max:,}, let me find the best options..."
            return response
        else:
            response += "\n\nWhat's your budget range in PKR?"
            return response
    
    def handle_comparison_request(self, session_id: str, message: str) -> str:
        """Handle laptop comparison requests"""
        message_lower = message.lower()
        
        # Extract laptop models or brands
        brands = self.extract_brands(message)
        
        if len(brands) >= 2:
            return f"""Great question! Let me compare {brands[0]} vs {brands[1]} for Pakistani market:

**{brands[0]}:**
• Pros: {"Strong build quality, good after-sales" if brands[0] == "HP" else "Reliable, good value" if brands[0] == "Dell" else "Best price-to-performance, good specs" if brands[0] == "Lenovo" else "Good displays, lightweight"}
• Cons: {"Slightly expensive" if brands[0] == "HP" else "Limited service centers" if brands[0] == "Dell" else "Build quality varies" if brands[0] == "Lenovo" else "Heating issues in some models"}
• Service: {"Excellent in major cities" if brands[0] in ["HP", "Dell"] else "Good availability" if brands[0] == "Lenovo" else "Limited centers"}

**{brands[1]}:**
• Pros: {"Strong build quality, good after-sales" if brands[1] == "HP" else "Reliable, good value" if brands[1] == "Dell" else "Best price-to-performance, good specs" if brands[1] == "Lenovo" else "Good displays, lightweight"}
• Cons: {"Slightly expensive" if brands[1] == "HP" else "Limited service centers" if brands[1] == "Dell" else "Build quality varies" if brands[1] == "Lenovo" else "Heating issues in some models"}

**For Pakistan:** HP and Dell have better service networks. Lenovo offers best value.

What's your budget and use case? I'll recommend the best model!"""
        
        return """I can help you compare laptops! 

Tell me:
1. Which specific models? (e.g., "HP 15s vs Lenovo IdeaPad 3")
2. Or which brands? (e.g., "HP vs Dell")
3. Your budget range?

I'll give you a detailed comparison with Pakistani market context!"""
    
    def handle_specific_laptop(self, session_id: str, message: str) -> str:
        """Handle questions about specific laptops"""
        # Try to find laptop in database
        brands = self.extract_brands(message)
        
        if brands:
            laptops = self.laptop_service.search_laptops(
                self.db,
                LaptopSearchParams(brand=brands[0])
            )
            
            if laptops:
                laptop = laptops[0]
                return f"""**{laptop.brand} {laptop.model}** - PKR {laptop.price_pkr:,}

**Specs:**
• Processor: {laptop.cpu}
• RAM: {laptop.ram_gb}GB
• Storage: {laptop.storage_gb}GB {laptop.storage_type}
• Display: {laptop.display_size}" 
• Graphics: {laptop.gpu}

**Ideal For:** {", ".join(laptop.ideal_for)}

**My Take:**
{"✅ Great for programming with good processor and RAM" if "Programming" in laptop.ideal_for else ""}
{"✅ Perfect budget option for students" if laptop.price_pkr < 90000 else ""}
{"✅ Premium build and performance" if laptop.price_pkr > 150000 else ""}

**Where to Buy:**
• Czone.pk - Usually best prices
• Paklap.pk - Good for comparisons
• Daraz.pk - Installment options available

Would you like to see alternatives or have questions?"""
        
        return """I'd love to help with that specific laptop!

Could you provide:
1. Full model name (e.g., "HP 15s-fq5327tu")
2. Or key specs you're asking about?

I can tell you if it's worth the price in Pakistani market!"""
    
    def handle_purchase_help(self, session_id: str, message: str) -> str:
        """Handle purchase guidance"""
        return """**Where to Buy Laptops in Pakistan** 🛒

**Online (Recommended):**
1. **Czone.pk** ⭐
   - Competitive prices
   - Karachi-based, reliable
   - Good customer service

2. **Paklap.pk**
   - Wide selection
   - Detailed specs
   - Lahore & Islamabad

3. **Daraz.pk**
   - 0% installments available
   - Buyer protection
   - Check seller ratings!

4. **Telemart.pk**
   - Good deals
   - Multiple payment options

**Physical Stores:**
• Hafeez Center (Lahore)
• Saddar (Karachi)
• Blue Area (Islamabad)

**Tips:**
✅ Always check warranty (1 year minimum)
✅ Compare prices across 2-3 sites
✅ Read reviews on PakWheels forums
✅ Avoid "too good to be true" deals
✅ Get invoice for warranty claims

**Payment:**
• Bank transfer (usually 2-3% discount)
• COD (cash on delivery)
• Credit card installments

Need help with a specific laptop purchase?"""
    
    def generate_response(self, session_id: str, message: str) -> Tuple[str, Optional[List]]:
        """Main method to generate contextual response"""
        # Update profile
        profile = self.update_profile(session_id, message)
        
        # Detect intent
        intent = self.detect_intent(message)
        
        # Get current step
        current_step = self.get_current_step(session_id)
        
        # Handle based on intent
        if intent == Intent.GREETING:
            response = self.handle_greeting(session_id)
            recommendations = None
        
        elif intent == Intent.BUDGET_QUERY:
            response = self.handle_budget_query(session_id, message, profile)
            recommendations = None
        
        elif intent == Intent.USE_CASE_QUERY:
            response = self.handle_use_case_query(session_id, message, profile)
            recommendations = None
        
        elif intent == Intent.COMPARISON_REQUEST:
            response = self.handle_comparison_request(session_id, message)
            recommendations = None
        
        elif intent == Intent.SPECIFIC_LAPTOP:
            response = self.handle_specific_laptop(session_id, message)
            recommendations = None
        
        elif intent == Intent.PURCHASE_HELP:
            response = self.handle_purchase_help(session_id, message)
            recommendations = None
        
        else:
            # Default flow based on current step
            if current_step == ConversationStep.GREETING:
                response = self.handle_greeting(session_id)
                recommendations = None
            
            elif current_step == ConversationStep.NEEDS_ANALYSIS:
                response = self.handle_use_case_query(session_id, message, profile)
                recommendations = None
            
            elif current_step == ConversationStep.BUDGET_CHECK:
                response = self.handle_budget_query(session_id, message, profile)
                recommendations = None
            
            elif current_step == ConversationStep.RECOMMENDATION:
                # Generate recommendations
                if profile.budget_max and profile.use_case:
                    laptops = self.get_recommendations(profile)
                    response = self.format_recommendations(profile, laptops)
                    recommendations = [self.laptop_to_dict(l) for l in laptops[:3]]
                    
                    # Mark recommendations shown
                    session = self.db.query(UserSession).filter(
                        UserSession.session_id == session_id
                    ).first()
                    if session:
                        session.preferences["recommendations_shown"] = True
                        self.db.commit()
                else:
                    response = "I need a bit more information. What's your budget and what will you use the laptop for?"
                    recommendations = None
            
            else:
                response = "I'm here to help! Ask me about laptops, budgets, or where to buy in Pakistan."
                recommendations = None
        
        # Add message to conversation history
        session = self.db.query(UserSession).filter(
            UserSession.session_id == session_id
        ).first()
        if session:
            session.conversation_history.append({
                "role": "user",
                "content": message,
                "timestamp": datetime.utcnow().isoformat()
            })
            session.conversation_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.utcnow().isoformat()
            })
            self.db.commit()
        
        return response, recommendations
    
    def get_recommendations(self, profile: UserProfile) -> List:
        """Get laptop recommendations based on profile"""
        from models.schemas import LaptopSearchParams
        
        # Build search params
        params = LaptopSearchParams(
            min_price=profile.budget_min,
            max_price=profile.budget_max,
            brand=profile.brand_pref[0] if profile.brand_pref else None,
            ideal_for=profile.use_case[0] if profile.use_case else None
        )
        
        laptops = self.laptop_service.search_laptops(self.db, params)
        
        # Sort by relevance
        return sorted(laptops, key=lambda x: x.price_pkr)[:5]
    
    def format_recommendations(self, profile: UserProfile, laptops: List) -> str:
        """Format laptop recommendations"""
        if not laptops:
            return f"""I couldn't find laptops matching your exact criteria (Budget: PKR {profile.budget_max:,}, Use: {', '.join(profile.use_case)}).

Try:
1. Increasing your budget by 10-20k
2. Considering refurbished options
3. Checking installment plans on Daraz

Would you like me to show nearby options?"""
        
        response = f"""**Perfect! Here are my top {len(laptops[:3])} recommendations for you:**\n\n"""
        
        if "Programming" in profile.use_case and profile.student_type == "FSC":
            response += "💡 *For FSC + Programming: Focus on RAM (8GB+) and processor (i5/Ryzen 5) for smooth coding experience*\n\n"
        
        response += "Check the laptop cards below for detailed specs and prices! 👇"
        
        return response
    
    def laptop_to_dict(self, laptop) -> Dict:
        """Convert laptop model to dictionary"""
        return {
            "id": laptop.id,
            "name": f"{laptop.brand} {laptop.model}",
            "brand": laptop.brand,
            "model": laptop.model,
            "processor": laptop.cpu,
            "ram": f"{laptop.ram_gb}GB",
            "storage": f"{laptop.storage_gb}GB {laptop.storage_type}",
            "display": f"{laptop.display_size}\"",
            "graphics": laptop.gpu,
            "price_pkr": laptop.price_pkr,
            "category": ", ".join(laptop.ideal_for),
            "url": laptop.source_url
        }
