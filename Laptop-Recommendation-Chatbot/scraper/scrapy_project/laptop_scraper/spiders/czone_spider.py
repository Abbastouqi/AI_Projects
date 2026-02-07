import scrapy
from laptop_scraper.items import LaptopItem
import re

class CzoneSpider(scrapy.Spider):
    name = 'czone'
    allowed_domains = ['czone.pk']
    start_urls = [
        'https://www.czone.pk/laptops-pakistan-ppt-1.html',
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
    }
    
    def parse(self, response):
        """Parse laptop listing page"""
        # Extract laptop product links
        laptop_links = response.css('div.product-item a.product-link::attr(href)').getall()
        
        for link in laptop_links:
            yield response.follow(link, callback=self.parse_laptop)
        
        # Follow pagination
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_laptop(self, response):
        """Parse individual laptop page"""
        item = LaptopItem()
        
        # Basic info
        item['full_name'] = response.css('h1.product-title::text').get()
        item['product_url'] = response.url
        item['source_site'] = 'czone.pk'
        
        # Extract brand and model from title
        title = item['full_name'] or ''
        brands = ['HP', 'Dell', 'Lenovo', 'ASUS', 'Acer', 'MSI']
        for brand in brands:
            if brand.lower() in title.lower():
                item['brand'] = brand
                item['model'] = title.replace(brand, '').strip()
                break
        
        # Price
        price_text = response.css('span.product-price::text').get()
        item['price_raw'] = price_text
        
        # Image
        item['image_url'] = response.css('img.product-image::attr(src)').get()
        
        # Specs - adjust selectors based on actual HTML structure
        specs = response.css('div.specifications table tr')
        
        for spec in specs:
            label = spec.css('td:first-child::text').get()
            value = spec.css('td:last-child::text').get()
            
            if not label or not value:
                continue
            
            label_lower = label.lower()
            
            if 'processor' in label_lower or 'cpu' in label_lower:
                item['cpu'] = value.strip()
            elif 'ram' in label_lower or 'memory' in label_lower:
                item['ram_raw'] = value.strip()
            elif 'storage' in label_lower or 'hard' in label_lower or 'ssd' in label_lower:
                item['storage_raw'] = value.strip()
            elif 'graphics' in label_lower or 'gpu' in label_lower:
                item['gpu'] = value.strip()
            elif 'display' in label_lower or 'screen' in label_lower:
                # Extract display size
                size_match = re.search(r'(\d+\.?\d*)\s*["\']', value)
                if size_match:
                    item['display_size'] = float(size_match.group(1))
            elif 'battery' in label_lower:
                # Extract battery hours
                hours_match = re.search(r'(\d+\.?\d*)\s*hours?', value, re.IGNORECASE)
                if hours_match:
                    item['battery_hours'] = float(hours_match.group(1))
            elif 'weight' in label_lower:
                # Extract weight
                weight_match = re.search(r'(\d+\.?\d*)\s*kg', value, re.IGNORECASE)
                if weight_match:
                    item['weight_kg'] = float(weight_match.group(1))
        
        # Availability
        availability = response.css('span.availability::text').get()
        item['availability'] = availability
        item['in_stock'] = 'in stock' in (availability or '').lower()
        
        # Set defaults if not found
        if not item.get('gpu'):
            item['gpu'] = 'Integrated Graphics'
        if not item.get('display_size'):
            item['display_size'] = 15.6
        
        yield item
