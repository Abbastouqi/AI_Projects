import scrapy
from laptop_scraper.items import LaptopItem
import re
import json

class TelemartSpider(scrapy.Spider):
    name = 'telemart'
    allowed_domains = ['telemart.pk']
    start_urls = [
        'https://www.telemart.pk/laptops/',
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }
    
    def parse(self, response):
        """Parse laptop listing page"""
        # Extract laptop product links
        laptop_links = response.css('div.product-card a.product-link::attr(href)').getall()
        
        for link in laptop_links:
            yield response.follow(link, callback=self.parse_laptop)
        
        # Follow pagination
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_laptop(self, response):
        """Parse individual laptop page"""
        item = LaptopItem()
        
        # Basic info
        item['full_name'] = response.css('h1.product-title::text').get()
        item['product_url'] = response.url
        item['source_site'] = 'telemart.pk'
        
        # Extract brand and model
        title = item['full_name'] or ''
        brands = ['HP', 'Dell', 'Lenovo', 'ASUS', 'Acer', 'MSI', 'Apple', 'Samsung']
        for brand in brands:
            if brand.lower() in title.lower():
                item['brand'] = brand
                item['model'] = title.replace(brand, '').strip()
                break
        
        # Price
        price_text = response.css('span.product-price::text').get()
        if not price_text:
            price_text = response.css('div.price-box span::text').get()
        item['price_raw'] = price_text
        
        # Image
        item['image_url'] = response.css('img.product-main-image::attr(src)').get()
        
        # Specs - Telemart often has structured data
        specs_json = response.css('script[type="application/ld+json"]::text').get()
        if specs_json:
            try:
                data = json.loads(specs_json)
                if 'offers' in data:
                    item['price_raw'] = str(data['offers'].get('price', ''))
            except:
                pass
        
        # Parse specs table
        spec_rows = response.css('table.specifications tr')
        
        for row in spec_rows:
            label = row.css('th::text').get()
            value = row.css('td::text').get()
            
            if not label or not value:
                continue
            
            label_lower = label.lower()
            
            if 'processor' in label_lower:
                item['cpu'] = value.strip()
            elif 'ram' in label_lower:
                item['ram_raw'] = value.strip()
            elif 'storage' in label_lower:
                item['storage_raw'] = value.strip()
            elif 'graphics' in label_lower:
                item['gpu'] = value.strip()
            elif 'screen' in label_lower or 'display' in label_lower:
                size_match = re.search(r'(\d+\.?\d*)\s*["\']', value)
                if size_match:
                    item['display_size'] = float(size_match.group(1))
            elif 'battery' in label_lower:
                hours_match = re.search(r'(\d+\.?\d*)\s*hours?', value, re.IGNORECASE)
                if hours_match:
                    item['battery_hours'] = float(hours_match.group(1))
            elif 'weight' in label_lower:
                weight_match = re.search(r'(\d+\.?\d*)\s*kg', value, re.IGNORECASE)
                if weight_match:
                    item['weight_kg'] = float(weight_match.group(1))
        
        # Availability
        availability = response.css('div.availability span::text').get()
        item['availability'] = availability
        item['in_stock'] = 'in stock' in (availability or '').lower()
        
        # Defaults
        if not item.get('gpu'):
            item['gpu'] = 'Integrated Graphics'
        if not item.get('display_size'):
            item['display_size'] = 15.6
        
        yield item
