import re
import json
from datetime import datetime
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add backend to path for database models
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../backend'))
from models.database import Laptop, Base


class DataCleaningPipeline:
    """Clean and normalize scraped data"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Clean RAM
        if adapter.get('ram_raw'):
            ram_match = re.search(r'(\d+)\s*GB', adapter['ram_raw'], re.IGNORECASE)
            if ram_match:
                adapter['ram_gb'] = int(ram_match.group(1))
            else:
                adapter['ram_gb'] = 8  # Default
        
        # Clean Storage
        if adapter.get('storage_raw'):
            storage_text = adapter['storage_raw']
            
            # Extract GB/TB
            storage_match = re.search(r'(\d+)\s*(GB|TB)', storage_text, re.IGNORECASE)
            if storage_match:
                size = int(storage_match.group(1))
                unit = storage_match.group(2).upper()
                adapter['storage_gb'] = size * 1024 if unit == 'TB' else size
            else:
                adapter['storage_gb'] = 256  # Default
            
            # Detect storage type
            if 'SSD' in storage_text.upper():
                adapter['storage_type'] = 'SSD'
            elif 'HDD' in storage_text.upper():
                adapter['storage_type'] = 'HDD'
            elif 'NVME' in storage_text.upper() or 'M.2' in storage_text.upper():
                adapter['storage_type'] = 'SSD'
            else:
                adapter['storage_type'] = 'SSD'  # Default to SSD for modern laptops
        
        # Clean Price
        if adapter.get('price_raw'):
            price_text = adapter['price_raw']
            
            # Check for "Call for price"
            if any(word in price_text.lower() for word in ['call', 'contact', 'inquiry']):
                adapter['price_available'] = False
                adapter['price_pkr'] = 0
            else:
                # Extract numbers
                price_match = re.search(r'[\d,]+', price_text.replace(',', ''))
                if price_match:
                    adapter['price_pkr'] = int(price_match.group(0).replace(',', ''))
                    adapter['price_available'] = True
                else:
                    adapter['price_available'] = False
                    adapter['price_pkr'] = 0
        
        # Extract CPU Generation
        if adapter.get('cpu'):
            cpu_text = adapter['cpu']
            
            # Intel generation (e.g., i5-1235U -> 12th gen)
            intel_match = re.search(r'i[357]-(\d{1,2})\d{2,3}', cpu_text)
            if intel_match:
                gen = int(intel_match.group(1))
                adapter['cpu_generation'] = f"{gen}th Gen Intel"
            
            # AMD Ryzen generation
            elif 'ryzen' in cpu_text.lower():
                ryzen_match = re.search(r'ryzen\s+[357]\s+(\d{1})(\d{3})', cpu_text, re.IGNORECASE)
                if ryzen_match:
                    gen = int(ryzen_match.group(1))
                    adapter['cpu_generation'] = f"Ryzen {gen}000 Series"
        
        # Extract brand from model name if not set
        if not adapter.get('brand') and adapter.get('full_name'):
            name = adapter['full_name']
            brands = ['HP', 'Dell', 'Lenovo', 'ASUS', 'Acer', 'MSI', 'Apple']
            for brand in brands:
                if brand.lower() in name.lower():
                    adapter['brand'] = brand
                    break
        
        # Set scraped timestamp
        adapter['scraped_at'] = datetime.utcnow().isoformat()
        
        return item


class CategoryDetectionPipeline:
    """Detect suitable use cases based on specs"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        categories = []
        
        ram = adapter.get('ram_gb', 0)
        storage = adapter.get('storage_gb', 0)
        cpu = adapter.get('cpu', '').lower()
        gpu = adapter.get('gpu', '').lower()
        price = adapter.get('price_pkr', 0)
        
        # Programming
        if ram >= 8 and ('i5' in cpu or 'i7' in cpu or 'ryzen 5' in cpu or 'ryzen 7' in cpu):
            categories.append('Programming')
        
        # Gaming
        if ('gtx' in gpu or 'rtx' in gpu or 'radeon rx' in gpu) and ram >= 8:
            categories.append('Gaming')
        elif 'dedicated' in gpu.lower() or 'nvidia' in gpu.lower():
            categories.append('Gaming')
        
        # Video Editing
        if ram >= 16 and ('i7' in cpu or 'ryzen 7' in cpu):
            categories.append('Video Editing')
        
        # Engineering
        if ram >= 8 and storage >= 512:
            categories.append('Engineering')
        
        # FSC Student / Basic Use
        if price < 90000 or ('i3' in cpu or 'ryzen 3' in cpu):
            categories.append('FSC Student')
            categories.append('Office Work')
        
        # Office Work
        if ram >= 4 and storage >= 256:
            if 'Office Work' not in categories:
                categories.append('Office Work')
        
        # CS Student
        if 'Programming' in categories:
            categories.append('CS Student')
        
        # Default
        if not categories:
            categories.append('General Use')
        
        adapter['ideal_for'] = categories
        
        return item


class JsonExportPipeline:
    """Export items to JSON file"""
    
    def open_spider(self, spider):
        self.items = []
    
    def close_spider(self, spider):
        # Get export path from settings
        export_path = spider.settings.get('EXPORT_JSON_PATH', 'laptops.json')
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, indent=2, ensure_ascii=False)
        
        spider.logger.info(f'Exported {len(self.items)} items to {export_path}')
    
    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item


class DatabasePipeline:
    """Insert items into PostgreSQL/SQLite database"""
    
    def open_spider(self, spider):
        # Get database URL from settings
        db_url = spider.settings.get('DATABASE_URL', 'sqlite:///./laptops.db')
        
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        spider.logger.info(f'Connected to database: {db_url}')
    
    def close_spider(self, spider):
        self.session.close()
        spider.logger.info('Database connection closed')
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Skip if price not available
        if not adapter.get('price_available', False):
            spider.logger.warning(f"Skipping {adapter.get('full_name')} - Price not available")
            return item
        
        # Check if laptop already exists
        existing = self.session.query(Laptop).filter(
            Laptop.brand == adapter.get('brand'),
            Laptop.model == adapter.get('model')
        ).first()
        
        if existing:
            # Update existing
            existing.price_pkr = adapter.get('price_pkr')
            existing.source_url = adapter.get('product_url')
            spider.logger.info(f"Updated: {adapter.get('full_name')}")
        else:
            # Create new
            laptop = Laptop(
                brand=adapter.get('brand', 'Unknown'),
                model=adapter.get('model', adapter.get('full_name', 'Unknown')),
                cpu=adapter.get('cpu', 'Unknown'),
                ram_gb=adapter.get('ram_gb', 8),
                storage_gb=adapter.get('storage_gb', 256),
                storage_type=adapter.get('storage_type', 'SSD'),
                gpu=adapter.get('gpu', 'Integrated'),
                display_size=adapter.get('display_size', 15.6),
                price_pkr=adapter.get('price_pkr', 0),
                battery_hours=adapter.get('battery_hours'),
                weight_kg=adapter.get('weight_kg'),
                ideal_for=adapter.get('ideal_for', ['General Use']),
                source_url=adapter.get('product_url')
            )
            self.session.add(laptop)
            spider.logger.info(f"Added: {adapter.get('full_name')}")
        
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Database error: {e}")
        
        return item
