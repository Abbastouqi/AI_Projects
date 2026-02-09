# Quick Start Guide - Database Setup

## Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 2: Create Environment File

```bash
copy .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-key-here
```

## Step 3: Initialize Database

```bash
python scripts/init_database.py
```

This will:
✅ Create SQLite database with 3 tables (Laptop, UserSession, Recommendation)
✅ Seed with 16 Pakistani laptops (HP, Dell, Lenovo, ASUS)
✅ Price range: PKR 72,000 - 225,000

## Step 4: Start Server

```bash
python main.py
```

Server runs at: http://localhost:8000

## Step 5: Test API

Open browser: http://localhost:8000/docs

Try these endpoints:
- `GET /api/laptops/` - List all laptops
- `GET /api/laptops/budget/80000/120000` - Budget filter
- `GET /api/laptops/category/Programming` - Category filter

## Database File

Location: `backend/laptop_recommendations.db`

View with SQLite browser or:
```bash
sqlite3 laptop_recommendations.db
.tables
SELECT * FROM laptops LIMIT 5;
```

## Sample Laptops Included

**Budget (60k-90k):**
- HP 15s-fq5007tu - 85k PKR
- Lenovo V15 G3 - 72k PKR
- Dell Inspiron 15 3520 - 89k PKR

**Mid-Range (100k-140k):**
- HP 15s-fq5327tu - 115k PKR
- Lenovo IdeaPad 3 - 108k PKR
- ASUS VivoBook 15 - 112k PKR

**Premium (200k+):**
- HP Envy x360 - 215k PKR
- Dell Inspiron 16 5630 - 225k PKR

## Next Steps

1. Start frontend: `cd frontend && npm install && npm run dev`
2. Test chat at: http://localhost:3000
3. Check `README_DATABASE.md` for detailed documentation
