import requests
from bs4 import BeautifulSoup
import json
import time

class LaptopScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.laptops = []
    
    def scrape_daraz(self):
        """Scrape laptop data from Daraz.pk"""
        # Example implementation - adjust selectors based on actual site
        url = "https://www.daraz.pk/laptops/"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Adjust selectors based on actual HTML structure
            products = soup.find_all('div', class_='product-item')
            
            for product in products[:20]:  # Limit to 20 items
                try:
                    name = product.find('div', class_='title').text.strip()
                    price_text = product.find('span', class_='price').text.strip()
                    price = int(''.join(filter(str.isdigit, price_text)))
                    
                    laptop = {
                        "name": name,
                        "brand": self._extract_brand(name),
                        "processor": "To be updated",
                        "ram": "To be updated",
                        "storage": "To be updated",
                        "display": "15.6\" FHD",
                        "graphics": "Integrated",
                        "price_pkr": price,
                        "category": "General",
                        "url": product.find('a')['href']
                    }
                    self.laptops.append(laptop)
                except Exception as e:
                    print(f"Error parsing product: {e}")
                    continue
                
                time.sleep(0.5)  # Be respectful
        
        except Exception as e:
            print(f"Error scraping: {e}")
    
    def _extract_brand(self, name):
        brands = ['HP', 'Dell', 'Lenovo', 'ASUS', 'Acer', 'MSI', 'Apple']
        for brand in brands:
            if brand.lower() in name.lower():
                return brand
        return "Unknown"
    
    def save_to_json(self, filename='../data/laptops.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.laptops, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(self.laptops)} laptops to {filename}")

if __name__ == "__main__":
    scraper = LaptopScraper()
    scraper.scrape_daraz()
    scraper.save_to_json()
