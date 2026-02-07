# Laptop Scraper for Pakistani E-commerce Sites

Professional Scrapy-based web scraper for extracting laptop data from Pakistani e-commerce websites.

## Features

✅ **Multi-site Support:**
- Czone.pk
- Paklap.pk
- Telemart.pk

✅ **Data Extraction:**
- Brand, model, full specs
- CPU (with generation detection)
- RAM (normalized to GB)
- Storage (normalized to GB, type detection)
- GPU
- Price in PKR (handles "Call for price")
- Product URLs and images
- Availability status

✅ **Smart Processing:**
- Data cleaning and normalization
- CPU generation extraction (Intel 12th gen, Ryzen 5000 series)
- Automatic category detection (Programming, Gaming, FSC Student, etc.)
- Rate limiting and user-agent rotation
- Duplicate detection

✅ **Export Options:**
- JSON file export
- Direct PostgreSQL/SQLite insertion
- Structured data format

## Installation

```bash
cd scraper
pip install -r requirements.txt
```

## Usage

### Run Individual Spider

```bash
cd scrapy_project

# Scrape Telemart
scrapy crawl telemart

# Scrape Paklap
scrapy crawl paklap

# Scrape Czone
scrapy crawl czone
```

### Run All Spiders

```bash
cd scrapy_project
scrapy crawl telemart
scrapy crawl paklap
scrapy crawl czone
```

### Custom Output

```bash
# Export to specific JSON file
scrapy crawl telemart -o laptops_telemart.json

# Export to CSV
scrapy crawl paklap -o laptops_paklap.csv

# Limit items
scrapy crawl czone -s CLOSESPIDER_ITEMCOUNT=50
```

## Configuration

Edit `scrapy_project/laptop_scraper/settings.py`:

```python
# Rate limiting
DOWNLOAD_DELAY = 2  # seconds between requests
CONCURRENT_REQUESTS = 8

# Database
DATABASE_URL = 'sqlite:///../../../backend/laptop_recommendations.db'

# Export path
EXPORT_JSON_PATH = '../../../data/scraped_laptops.json'
```

## Data Pipeline

1. **DataCleaningPipeline**: Normalizes RAM, storage, price
2. **CategoryDetectionPipeline**: Detects ideal use cases
3. **JsonExportPipeline**: Exports to JSON
4. **DatabasePipeline**: Inserts into database

## Category Detection Logic

```python
Programming: RAM >= 8GB + (i5/i7 or Ryzen 5/7)
Gaming: Dedicated GPU + RAM >= 8GB
Video Editing: RAM >= 16GB + (i7 or Ryzen 7)
FSC Student: Price < 90k or (i3 or Ryzen 3)
Engineering: RAM >= 8GB + Storage >= 512GB
```

## Data Cleaning Examples

**RAM Normalization:**
- "8GB DDR4" → 8
- "16 GB" → 16

**Storage Normalization:**
- "512GB SSD" → 512 (GB), "SSD"
- "1TB HDD" → 1024 (GB), "HDD"

**Price Cleaning:**
- "Rs. 125,000" → 125000
- "PKR 85000" → 85000
- "Call for price" → 0 (skipped)

**CPU Generation:**
- "Intel Core i5-1235U" → "12th Gen Intel"
- "AMD Ryzen 5 5500U" → "Ryzen 5000 Series"

## Avoiding Blocks

The scraper includes:
- User-agent rotation (4 different agents)
- Random delays (2-4 seconds)
- Respects robots.txt
- HTTP caching
- Auto-throttling

## Output Format

### JSON Export
```json
{
  "brand": "HP",
  "model": "15s-fq5327tu",
  "cpu": "Intel Core i5-1235U",
  "cpu_generation": "12th Gen Intel",
  "ram_gb": 8,
  "storage_gb": 512,
  "storage_type": "SSD",
  "gpu": "Intel Iris Xe Graphics",
  "display_size": 15.6,
  "price_pkr": 115000,
  "ideal_for": ["Programming", "CS Student"],
  "source_site": "telemart.pk",
  "product_url": "https://...",
  "in_stock": true
}
```

### Database Schema
Data is inserted into the `laptops` table with all fields mapped.

## Troubleshooting

**No items scraped:**
- Check if website structure changed
- Verify CSS selectors in spider
- Check robots.txt compliance

**Database errors:**
- Ensure database exists: `python backend/scripts/init_database.py`
- Check DATABASE_URL in settings.py

**Rate limiting:**
- Increase DOWNLOAD_DELAY
- Reduce CONCURRENT_REQUESTS

## Extending

### Add New Site

1. Create spider: `scraper/scrapy_project/laptop_scraper/spiders/newsite_spider.py`
2. Implement `parse()` and `parse_laptop()` methods
3. Map CSS selectors to item fields
4. Run: `scrapy crawl newsite`

### Custom Pipeline

Add to `pipelines.py`:
```python
class CustomPipeline:
    def process_item(self, item, spider):
        # Your logic
        return item
```

Enable in `settings.py`:
```python
ITEM_PIPELINES = {
    'laptop_scraper.pipelines.CustomPipeline': 150,
}
```

## Legal & Ethics

- Respects robots.txt
- Rate-limited to avoid server load
- For educational/personal use
- Check website terms of service
- Don't resell scraped data

## Maintenance

Update selectors when websites change:
1. Inspect website HTML
2. Update CSS selectors in spider
3. Test with: `scrapy crawl spider_name -s CLOSESPIDER_ITEMCOUNT=1`

## Performance

- ~100-200 laptops/hour (with delays)
- Memory efficient (streaming)
- Handles pagination automatically
- Duplicate detection built-in
