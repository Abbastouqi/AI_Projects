import scrapy
from laptop_scraper.items import LaptopItem
import re

class PaklapSpider(scrapy.Spider):
    name = 'paklap'
    allowed_domains = ['paklap.pk']
    start_urls = [
        'https://www.paklap.pk/laptops.html',
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
    }
    
    def parse(self, response):
        """Parse laptop listing page"""
        # Extract laptop product links
        laptop_links = response.css('div.product-item h3 a::attr(href)').getall()
        
        for link in laptop_links:
            yield response.follow(link, callback=self.parse_laptop)
        
        # Follow pagination
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_laptop(self, response):
        """Parse individual laptop page"""
        item = LaptopItem()
        
        # Basic info
        item['full_name'] = response.css('h1.product-name::text').get()
        item['product_url'] = response.url
        item['source_site'] = 'paklap.pk'
        
        # Extract brand and model
        title = item['full_name'] or ''
        brands = ['HP', 'Dell', 'Lenovo', 'ASUS', 'Acer', 'MSI', 'Apple']
        for brand in brands:
            if brand.lower() in title.lower():
                item['brand'] = brand
                item['model'] = title.replace(brand, '').strip()
                break
        
        # Price
        price_text = response.css('span.price::text').get()
        item['price_raw'] = price_text
        
        # Image
        item['image_url'] = response.css('img.main-image::attr(src)').get()
        
        # Specs from description or table
        spec_items = response.css('div.product-specs li')
        
        for spec_item in spec_items:
            text = spec_item.css('::text').get()
            if not text:
                continue
            
            text_lower = text.lower()
            
            if 'processor' in text_lower:
                item['cpu'] = text.split(':')[-1].strip()
            elif 'ram' in text_lower:
                item['ram_raw'] = text.split(':')[-1].strip()
            elif 'storage' in text_lower or 'ssd' in text_lower or 'hdd' in text_lower:
                item['storage_raw'] = text.split(':')[-1].strip()
            elif 'graphics' in text_lower:
                item['gpu'] = text.split(':')[-1].strip()
            elif 'display' in text_lower:
                size_match = re.search(r'(\d+\.?\d*)\s*["\']', text)
                if size_match:
                    item['display_size'] = float(size_match.group(1))
        
        # Availability
        stock_status = response.css('span.stock-status::text').get()
        item['availability'] = stock_status
        item['in_stock'] = 'in stock' in (stock_status or '').lower()
        
        # Defaults
        if not item.get('gpu'):
            item['gpu'] = 'Integrated Graphics'
        if not item.get('display_size'):
            item['display_size'] = 15.6
        
        yield item
