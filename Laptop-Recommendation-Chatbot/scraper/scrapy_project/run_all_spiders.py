"""
Script to run all spiders sequentially
"""
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from laptop_scraper.spiders.telemart_spider import TelemartSpider
from laptop_scraper.spiders.paklap_spider import PaklapSpider
from laptop_scraper.spiders.czone_spider import CzoneSpider

def run_all_spiders():
    """Run all spiders one after another"""
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    
    # Add all spiders
    process.crawl(TelemartSpider)
    process.crawl(PaklapSpider)
    process.crawl(CzoneSpider)
    
    # Start crawling
    process.start()
    
    print("\n✅ All spiders completed!")
    print("Check data/scraped_laptops.json for results")
    print("Check backend/laptop_recommendations.db for database entries")

if __name__ == '__main__':
    print("🕷️  Starting all laptop scrapers...")
    print("This will scrape: Telemart, Paklap, Czone")
    print("Estimated time: 30-60 minutes\n")
    
    run_all_spiders()
