BOT_NAME = 'laptop_scraper'

SPIDER_MODULES = ['laptop_scraper.spiders']
NEWSPIDER_MODULE = 'laptop_scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# Configure a delay for requests (in seconds)
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True

# Disable cookies
COOKIES_ENABLED = False

# Disable Telnet Console
TELNETCONSOLE_ENABLED = False

# Override the default request headers
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.9',
}

# Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {
   'laptop_scraper.middlewares.LaptopScraperSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
   'laptop_scraper.middlewares.RotateUserAgentMiddleware': 400,
   'laptop_scraper.middlewares.LaptopScraperDownloaderMiddleware': 543,
}

# Configure item pipelines
ITEM_PIPELINES = {
   'laptop_scraper.pipelines.DataCleaningPipeline': 100,
   'laptop_scraper.pipelines.CategoryDetectionPipeline': 200,
   'laptop_scraper.pipelines.JsonExportPipeline': 300,
   'laptop_scraper.pipelines.DatabasePipeline': 400,
}

# User agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

# AutoThrottle settings
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# Database settings
DATABASE_URL = 'sqlite:///../../../backend/laptop_recommendations.db'

# Export settings
EXPORT_JSON_PATH = '../../../data/scraped_laptops.json'

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 408, 429]
