import scrapy

class LaptopItem(scrapy.Item):
    # Basic Info
    brand = scrapy.Field()
    model = scrapy.Field()
    full_name = scrapy.Field()
    
    # Specs
    cpu = scrapy.Field()
    cpu_generation = scrapy.Field()
    ram_gb = scrapy.Field()
    ram_raw = scrapy.Field()
    storage_gb = scrapy.Field()
    storage_type = scrapy.Field()
    storage_raw = scrapy.Field()
    gpu = scrapy.Field()
    display_size = scrapy.Field()
    
    # Pricing
    price_pkr = scrapy.Field()
    price_raw = scrapy.Field()
    price_available = scrapy.Field()
    
    # URLs and Images
    product_url = scrapy.Field()
    image_url = scrapy.Field()
    
    # Availability
    availability = scrapy.Field()
    in_stock = scrapy.Field()
    
    # Source
    source_site = scrapy.Field()
    scraped_at = scrapy.Field()
    
    # Detected Categories
    ideal_for = scrapy.Field()
    
    # Additional
    battery_hours = scrapy.Field()
    weight_kg = scrapy.Field()
