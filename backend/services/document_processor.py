"""
Document processor for creating searchable laptop documents
Combines specs with expert advice for better RAG retrieval
"""
from typing import List, Dict, Any
from dataclasses import dataclass
import json

@dataclass
class LaptopDocument:
    """Structured document for laptop information"""
    laptop_id: int
    content: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "laptop_id": self.laptop_id,
            "content": self.content,
            "metadata": self.metadata
        }

class DocumentProcessor:
    """Process laptop data into searchable documents"""
    
    # Expert advice templates for different use cases
    EXPERT_ADVICE = {
        "FSC Student": "Ideal for FSC students who need reliable performance for document work, online classes, and basic computing. Focus on battery life and portability.",
        "Programming": "Perfect for programming students and developers. Good CPU performance for compiling code, sufficient RAM for IDEs and virtual machines, and SSD for fast file operations.",
        "CS Student": "Excellent for Computer Science students. Handles programming, data structures, algorithms, and light development work efficiently.",
        "Engineering": "Suitable for engineering students running CAD software, simulations, and technical applications. Requires good CPU and adequate RAM.",
        "Data Science": "Great for data science work with Python, Jupyter notebooks, and machine learning libraries. Benefits from higher RAM and good CPU performance.",
        "Machine Learning": "Optimized for machine learning tasks, model training, and data processing. Requires powerful CPU, high RAM, and ideally dedicated GPU.",
        "Gaming": "Built for gaming with dedicated graphics card and high refresh rate display. Also excellent for video editing and 3D work.",
        "Video Editing": "Powerful enough for video editing and content creation. Good CPU, high RAM, and dedicated GPU recommended.",
        "Graphic Design": "Suitable for graphic design work with Adobe Creative Suite. Good display quality and adequate performance.",
        "Office Work": "Perfect for office productivity, document editing, spreadsheets, and presentations. Reliable and efficient.",
        "Business": "Professional laptop for business use with good build quality, battery life, and performance.",
        "Basic Computing": "Great for everyday tasks like web browsing, email, and media consumption. Budget-friendly option."
    }
    
    @staticmethod
    def create_laptop_document(laptop_data: Dict[str, Any]) -> LaptopDocument:
        """
        Create a rich document from laptop data
        Combines specs with expert advice for better semantic search
        """
        # Extract key information
        laptop_id = laptop_data.get("id")
        brand = laptop_data.get("brand", "")
        model = laptop_data.get("model", "")
        cpu = laptop_data.get("cpu", "")
        ram_gb = laptop_data.get("ram_gb", 0)
        storage_gb = laptop_data.get("storage_gb", 0)
        storage_type = laptop_data.get("storage_type", "")
        gpu = laptop_data.get("gpu", "")
        display_size = laptop_data.get("display_size", 0)
        price_pkr = laptop_data.get("price_pkr", 0)
        battery_hours = laptop_data.get("battery_hours")
        weight_kg = laptop_data.get("weight_kg")
        ideal_for = laptop_data.get("ideal_for", [])
        
        # Build rich content for embedding
        content_parts = []
        
        # Title and brand
        content_parts.append(f"Laptop: {brand} {model}")
        
        # Price information
        price_category = DocumentProcessor._categorize_price(price_pkr)
        content_parts.append(f"Price: PKR {price_pkr:,} ({price_category} range)")
        
        # Processor details
        cpu_category = DocumentProcessor._categorize_cpu(cpu)
        content_parts.append(f"Processor: {cpu} - {cpu_category} performance")
        
        # Memory and storage
        ram_category = DocumentProcessor._categorize_ram(ram_gb)
        content_parts.append(f"Memory: {ram_gb}GB RAM - {ram_category}")
        content_parts.append(f"Storage: {storage_gb}GB {storage_type} - Fast and reliable")
        
        # Graphics
        gpu_category = DocumentProcessor._categorize_gpu(gpu)
        content_parts.append(f"Graphics: {gpu} - {gpu_category}")
        
        # Display
        content_parts.append(f"Display: {display_size}\" screen")
        
        # Battery and portability
        if battery_hours:
            battery_desc = DocumentProcessor._categorize_battery(battery_hours)
            content_parts.append(f"Battery: {battery_hours} hours - {battery_desc}")
        
        if weight_kg:
            portability = DocumentProcessor._categorize_weight(weight_kg)
            content_parts.append(f"Weight: {weight_kg}kg - {portability}")
        
        # Use cases with expert advice
        if ideal_for:
            content_parts.append(f"\nIdeal for: {', '.join(ideal_for)}")
            
            # Add expert advice for each use case
            for use_case in ideal_for:
                if use_case in DocumentProcessor.EXPERT_ADVICE:
                    content_parts.append(DocumentProcessor.EXPERT_ADVICE[use_case])
        
        # Value proposition
        value_prop = DocumentProcessor._generate_value_proposition(
            price_pkr, ram_gb, storage_type, cpu, ideal_for
        )
        content_parts.append(f"\n{value_prop}")
        
        # Combine all parts
        content = "\n".join(content_parts)
        
        # Metadata for filtering
        metadata = {
            "laptop_id": laptop_id,
            "brand": brand,
            "model": model,
            "price_pkr": price_pkr,
            "price_category": price_category,
            "ram_gb": ram_gb,
            "storage_type": storage_type,
            "ideal_for": ideal_for,
            "cpu_category": cpu_category,
            "gpu_category": gpu_category
        }
        
        return LaptopDocument(
            laptop_id=laptop_id,
            content=content,
            metadata=metadata
        )
    
    @staticmethod
    def _categorize_price(price: int) -> str:
        """Categorize price range"""
        if price < 80000:
            return "Budget-friendly"
        elif price < 120000:
            return "Mid-range"
        elif price < 180000:
            return "Premium"
        else:
            return "High-end"
    
    @staticmethod
    def _categorize_cpu(cpu: str) -> str:
        """Categorize CPU performance"""
        cpu_lower = cpu.lower()
        if "i3" in cpu_lower or "ryzen 3" in cpu_lower:
            return "Good for basic tasks and light multitasking"
        elif "i5" in cpu_lower or "ryzen 5" in cpu_lower:
            return "Excellent for programming, multitasking, and productivity"
        elif "i7" in cpu_lower or "ryzen 7" in cpu_lower:
            return "Powerful for demanding applications and heavy workloads"
        elif "i9" in cpu_lower or "ryzen 9" in cpu_lower:
            return "Top-tier performance for professional work"
        return "Reliable performance"
    
    @staticmethod
    def _categorize_ram(ram_gb: int) -> str:
        """Categorize RAM capacity"""
        if ram_gb <= 4:
            return "Basic multitasking"
        elif ram_gb == 8:
            return "Good for most tasks and programming"
        elif ram_gb == 16:
            return "Excellent for heavy multitasking and development"
        else:
            return "Professional-grade multitasking"
    
    @staticmethod
    def _categorize_gpu(gpu: str) -> str:
        """Categorize GPU type"""
        gpu_lower = gpu.lower()
        if "nvidia" in gpu_lower or "geforce" in gpu_lower or "rtx" in gpu_lower or "gtx" in gpu_lower:
            return "Dedicated graphics for gaming and creative work"
        elif "amd radeon" in gpu_lower and "graphics" not in gpu_lower:
            return "Dedicated AMD graphics"
        else:
            return "Integrated graphics for everyday use"
    
    @staticmethod
    def _categorize_battery(hours: float) -> str:
        """Categorize battery life"""
        if hours < 5:
            return "Moderate battery life"
        elif hours < 8:
            return "Good battery life for all-day use"
        else:
            return "Excellent battery life"
    
    @staticmethod
    def _categorize_weight(weight_kg: float) -> str:
        """Categorize portability"""
        if weight_kg < 1.5:
            return "Highly portable"
        elif weight_kg < 2.0:
            return "Good portability"
        else:
            return "Standard portability"
    
    @staticmethod
    def _generate_value_proposition(
        price: int,
        ram: int,
        storage_type: str,
        cpu: str,
        ideal_for: List[str]
    ) -> str:
        """Generate value proposition based on specs"""
        props = []
        
        if price < 90000 and ram >= 8 and storage_type == "SSD":
            props.append("Excellent value for money with modern specs")
        
        if ram >= 16:
            props.append("High RAM capacity for professional work")
        
        if storage_type == "SSD":
            props.append("Fast SSD storage for quick boot and app loading")
        
        if "i7" in cpu or "Ryzen 7" in cpu:
            props.append("Powerful processor for demanding tasks")
        
        if "Programming" in ideal_for or "CS Student" in ideal_for:
            props.append("Developer-friendly configuration")
        
        return " | ".join(props) if props else "Reliable laptop for everyday use"
    
    @staticmethod
    def batch_create_documents(laptops: List[Dict[str, Any]]) -> List[LaptopDocument]:
        """Create documents for multiple laptops"""
        return [
            DocumentProcessor.create_laptop_document(laptop)
            for laptop in laptops
        ]
