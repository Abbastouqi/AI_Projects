# Database Documentation

## Overview
This project uses SQLAlchemy ORM with SQLite (default) for the laptop recommendation system.

## Database Schema

### Tables

#### 1. Laptop
Stores laptop specifications and pricing information.

**Columns:**
- `id` (Integer, Primary Key): Auto-incrementing ID
- `brand` (String): Laptop brand (HP, Dell, Lenovo, ASUS)
- `model` (String): Model name
- `cpu` (String): Processor details
- `ram_gb` (Integer): RAM in GB
- `storage_gb` (Integer): Storage capacity in GB
- `storage_type` (String): SSD, HDD, or Hybrid
- `gpu` (String): Graphics card details
- `display_size` (Float): Screen size in inches
- `price_pkr` (Integer): Price in Pakistani Rupees
- `battery_hours` (Float, Optional): Battery life in hours
- `weight_kg` (Float, Optional): Weight in kilograms
- `ideal_for` (JSON Array): Categories like ["FSC Student", "Programming"]
- `source_url` (String, Optional): Product URL
- `created_at` (DateTime): Timestamp

**Relationships:**
- One-to-Many with Recommendation

#### 2. UserSession
Tracks user conversations and preferences.

**Columns:**
- `session_id` (String, Primary Key): Unique session identifier
- `conversation_history` (JSON Array): Chat messages
- `preferences` (JSON Object): User preferences (budget, field, etc.)
- `created_at` (DateTime): Timestamp

**Relationships:**
- One-to-Many with Recommendation

#### 3. Recommendation
Tracks which laptops were recommended to users.

**Columns:**
- `id` (Integer, Primary Key): Auto-incrementing ID
- `session_id` (String, Foreign Key): References UserSession
- `laptop_id` (Integer, Foreign Key): References Laptop
- `rank` (Integer): Recommendation rank (1, 2, 3)
- `reason_generated` (Text, Optional): AI-generated explanation
- `clicked` (Boolean): Whether user clicked the recommendation
- `created_at` (DateTime): Timestamp

**Relationships:**
- Many-to-One with UserSession
- Many-to-One with Laptop

## Setup Instructions

### 1. Initialize Database

```bash
cd backend
python scripts/init_database.py
```

This will:
- Create all tables
- Seed with 16 sample Pakistani laptops
- Display summary statistics

### 2. Database Location

Default: `backend/laptop_recommendations.db`

To use PostgreSQL or MySQL, update `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
# or
DATABASE_URL=mysql://user:password@localhost/dbname
```

## Sample Data

The seed script includes 16 realistic Pakistani laptops:

**Budget Range (60k-90k PKR):**
- HP 15s-fq5007tu - 85k
- Lenovo V15 G3 - 72k
- Dell Inspiron 15 3520 - 89k

**Mid-Range (100k-140k PKR):**
- HP 15s-fq5327tu - 115k
- Lenovo IdeaPad 3 - 108k
- Dell Inspiron 15 3530 - 125k
- ASUS VivoBook 15 - 112k

**High-End (140k-200k+ PKR):**
- HP Pavilion 15 - 175k
- Dell Inspiron 15 5530 - 185k
- HP Envy x360 - 215k
- Dell Inspiron 16 5630 - 225k

## API Endpoints

### Laptop Endpoints

```
GET    /api/laptops/                    # List all laptops
GET    /api/laptops/{id}                # Get laptop by ID
POST   /api/laptops/                    # Create laptop
PUT    /api/laptops/{id}                # Update laptop
DELETE /api/laptops/{id}                # Delete laptop
POST   /api/laptops/search              # Search with filters
GET    /api/laptops/budget/{min}/{max}  # Filter by budget
GET    /api/laptops/category/{category} # Filter by category
GET    /api/laptops/popular/top         # Most recommended
```

### Example Queries

**Search by budget:**
```bash
curl http://localhost:8000/api/laptops/budget/80000/120000
```

**Search by category:**
```bash
curl http://localhost:8000/api/laptops/category/Programming
```

**Advanced search:**
```bash
curl -X POST http://localhost:8000/api/laptops/search \
  -H "Content-Type: application/json" \
  -d '{
    "brand": "HP",
    "min_price": 80000,
    "max_price": 150000,
    "min_ram": 8,
    "ideal_for": "Programming"
  }'
```

## Service Layer

The project uses a service layer pattern:

- `LaptopService`: CRUD operations for laptops
- `SessionService`: User session management
- `RecommendationService`: Recommendation tracking

## Testing

Run unit tests:
```bash
cd backend
pip install pytest
pytest tests/test_models.py -v
```

## Migration (Future)

For production, use Alembic for migrations:

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Performance Tips

1. **Indexes**: Brand and price_pkr are indexed for faster queries
2. **JSON Queries**: Use SQLAlchemy's JSON operators for ideal_for filtering
3. **Pagination**: Always use skip/limit for large datasets
4. **Connection Pooling**: Configure for production workloads

## Backup

SQLite backup:
```bash
sqlite3 laptop_recommendations.db ".backup backup.db"
```

PostgreSQL backup:
```bash
pg_dump dbname > backup.sql
```
