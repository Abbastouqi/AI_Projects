# AI Laptop Recommendation Chatbot for Pakistani Students

An intelligent, context-aware chatbot that recommends laptops based on student needs using advanced conversation flow management and RAG (Retrieval Augmented Generation).

## 🌟 Key Features

### 💬 Intelligent Conversation Flow
- **Intent Detection**: Automatically classifies user messages (greeting, budget, use case, comparison, purchase help)
- **State Management**: Tracks conversation progress from greeting → needs analysis → budget → recommendations
- **User Profiling**: Remembers student type (FSC/Uni), major, use case, budget, and brand preferences
- **Context-Aware**: References previous messages and maintains conversation history
- **Pakistani Market Context**: Includes local pricing from Czone, Paklap, Daraz

### 🎨 Modern Chat Interface
- Dark-themed UI with glassmorphism effects
- Animated laptop hero section
- Quick reply buttons (FSC Student, Programming, 80k Budget, etc.)
- Laptop comparison view (select 2-3 laptops side-by-side)
- Session persistence with localStorage
- Typing indicators and smooth animations
- Fully responsive mobile design

### 🕷️ Professional Web Scraper
- Scrapes Pakistani e-commerce sites (Czone.pk, Paklap.pk, Telemart.pk)
- Extracts full specs: CPU, RAM, Storage, GPU, Display, Price
- Smart data cleaning and normalization
- CPU generation detection (Intel 12th gen, Ryzen 5000)
- Auto-categorization (Programming, Gaming, FSC Student, Video Editing)
- Rate limiting and user-agent rotation
- Direct PostgreSQL/SQLite insertion

### 🗄️ Robust Database
- SQLAlchemy ORM with 3 tables (Laptop, UserSession, Recommendation)
- 16 sample Pakistani laptops (72k - 225k PKR)
- Full CRUD API with FastAPI
- Budget filtering, category search
- Recommendation tracking and analytics

## 🚀 Quick Start

### 1. Backend Setup (2 minutes)

```bash
cd backend
pip install -r requirements.txt
copy .env.example .env
# Add your OpenAI API key to .env
python scripts/init_database.py
python main.py
```

Backend runs at: http://localhost:8000

### 2. Frontend Setup (2 minutes)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:3000

### 3. Try It Out!

Open http://localhost:3000 and chat:
- "I'm an FSC student with 80k budget"
- "I need a laptop for programming"
- "Compare HP vs Dell laptops"

## 📋 Project Structure

```
├── backend/                    # FastAPI backend
│   ├── api/                   # API routes
│   │   ├── routes.py         # Chat endpoints
│   │   └── laptop_routes.py  # Laptop CRUD
│   ├── core/                  # Configuration
│   ├── models/                # SQLAlchemy models & Pydantic schemas
│   │   ├── database.py       # Laptop, UserSession, Recommendation
│   │   ├── schemas.py        # API validation schemas
│   │   └── seed_data.py      # 16 sample Pakistani laptops
│   ├── services/              # Business logic
│   │   ├── conversation_manager.py  # Intent detection & flow
│   │   ├── laptop_service.py        # Laptop operations
│   │   └── rag_service.py           # RAG with ChromaDB
│   ├── scripts/               # Utility scripts
│   │   └── init_database.py  # Database initialization
│   └── tests/                 # Unit tests
├── frontend/                   # Next.js 14 frontend
│   ├── app/                   # App router
│   │   ├── page.tsx          # Home page
│   │   ├── layout.tsx        # Root layout
│   │   └── globals.css       # Global styles
│   ├── components/            # React components
│   │   ├── ChatInterface.tsx      # Main chat
│   │   ├── MessageBubble.tsx      # Message display
│   │   ├── LaptopCard.tsx         # Laptop specs card
│   │   ├── QuickReplies.tsx       # Quick reply buttons
│   │   └── ComparisonView.tsx     # Side-by-side comparison
│   └── types/                 # TypeScript types
├── scraper/                    # Scrapy web scraper
│   ├── scrapy_project/
│   │   └── laptop_scraper/
│   │       ├── spiders/       # Site-specific spiders
│   │       │   ├── czone_spider.py
│   │       │   ├── paklap_spider.py
│   │       │   └── telemart_spider.py
│   │       ├── pipelines.py   # Data cleaning & DB insertion
│   │       ├── items.py       # Data structure
│   │       └── settings.py    # Scraper configuration
│   └── run_all_spiders.py     # Run all scrapers
└── data/                       # Data storage
    └── laptops.json           # Sample laptop data
```

## 🎯 Conversation Flow System

### Intent Detection
The system automatically detects user intent:
- **Greeting**: "hi", "hello", "salam"
- **Budget Query**: "80k to 120k", "budget 100000"
- **Use Case**: "programming", "fsc student", "gaming"
- **Comparison**: "compare", "hp vs dell"
- **Purchase Help**: "where to buy", "czone", "daraz"

### State Management
Tracks conversation progress:
1. **Greeting** → Welcome message
2. **Needs Analysis** → Ask about use case
3. **Budget Check** → Determine price range
4. **Recommendation** → Show matching laptops
5. **Comparison** → Compare selected laptops

### User Profiling
Remembers throughout conversation:
- Student type (FSC, University)
- Major (CS, Engineering, Medical)
- Use cases (Programming, Gaming, Office)
- Budget range (min/max in PKR)
- Brand preferences (HP, Dell, Lenovo)

### Example Flow

```
User: "Hi"
Bot: [Greeting] "السلام علیکم! Welcome to Pakistan's smartest laptop assistant..."

User: "I'm an FSC pre-engineering student"
Bot: [Detects student_type=FSC] "What's your budget in PKR?"

User: "Around 80k"
Bot: [Extracts budget=80k±20%] Shows budget recommendations + refurbished options

User: "I also need it for programming"
Bot: [Updates use_case] Emphasizes RAM and processor, shows suitable laptops
```

## 🕷️ Web Scraper Usage

### Run Individual Spider
```bash
cd scraper/scrapy_project
scrapy crawl telemart  # Scrape Telemart.pk
scrapy crawl paklap    # Scrape Paklap.pk
scrapy crawl czone     # Scrape Czone.pk
```

### Run All Spiders
```bash
cd scraper/scrapy_project
python run_all_spiders.py
```

### Data Processing
- **RAM**: "8GB DDR4" → 8
- **Storage**: "512GB SSD" → 512, "SSD"
- **Price**: "Rs. 125,000" → 125000
- **CPU Gen**: "i5-1235U" → "12th Gen Intel"

### Auto-Categorization
- **Programming**: RAM ≥ 8GB + i5/Ryzen 5
- **Gaming**: Dedicated GPU + RAM ≥ 8GB
- **FSC Student**: Price < 90k or i3/Ryzen 3
- **Video Editing**: RAM ≥ 16GB + i7/Ryzen 7

## 🎨 Frontend Features

### Chat Interface
- Session persistence (localStorage)
- Auto-scroll to latest message
- Loading states with typing indicator
- Quick reply buttons for common queries

### Laptop Cards
- Gradient design with specs
- Price badge in PKR
- Compare button
- View details link

### Comparison View
- Side-by-side spec comparison
- Winner badge (best value)
- Modal overlay with glassmorphism

## 🗄️ Database

### Sample Data
16 Pakistani laptops included:
- **Budget (60k-90k)**: HP 15s, Lenovo V15, Dell Inspiron
- **Mid-range (100k-140k)**: HP Pavilion, Lenovo IdeaPad, ASUS VivoBook
- **Premium (150k+)**: HP Envy, Dell Inspiron 16, Lenovo ThinkBook

### API Endpoints
```
POST /api/chat                        # Chat with bot
GET  /api/laptops/                    # List all laptops
GET  /api/laptops/budget/80000/120000 # Filter by budget
GET  /api/laptops/category/Programming # Filter by category
POST /api/laptops/search              # Advanced search
GET  /api/session/{session_id}        # Get conversation history
```

## 🔧 Tech Stack

**Backend:**
- FastAPI (API framework)
- SQLAlchemy (ORM)
- OpenAI GPT-4 (AI recommendations)
- ChromaDB (Vector store)
- LangChain (RAG pipeline)

**Frontend:**
- Next.js 14 (React framework)
- TypeScript (Type safety)
- Tailwind CSS (Styling)
- Axios (HTTP client)

**Scraper:**
- Scrapy (Web scraping)
- BeautifulSoup (HTML parsing)
- SQLAlchemy (Database)

## 📚 Documentation

- **Complete Setup**: `COMPLETE_SETUP_GUIDE.md`
- **Database Guide**: `backend/README_DATABASE.md`
- **Scraper Guide**: `scraper/README_SCRAPER.md`
- **Quick Start**: `backend/QUICKSTART.md`

## 🎓 Use Cases

### FSC Pre-Engineering Student
- Budget: 70k-90k PKR
- Needs: Notes, PDFs, online classes
- Recommendation: HP 15s, Lenovo V15 (i3, 8GB RAM)

### CS/Programming Student
- Budget: 100k-140k PKR
- Needs: IDEs, compilers, multitasking
- Recommendation: Lenovo IdeaPad 3, HP 15s (i5, 8GB+ RAM, SSD)

### Engineering Student
- Budget: 140k-200k PKR
- Needs: CAD, MATLAB, heavy software
- Recommendation: HP Pavilion, Dell Inspiron (i7, 16GB RAM)

## 🌟 Pakistani Market Context

### Trusted Sellers
- **Czone.pk**: Competitive prices, Karachi-based
- **Paklap.pk**: Wide selection, Lahore & Islamabad
- **Daraz.pk**: 0% installments, buyer protection
- **Telemart.pk**: Good deals, multiple payment options

### Service Centers
- **HP**: Excellent in major cities
- **Dell**: Good availability
- **Lenovo**: Decent coverage
- **ASUS**: Limited centers

## 🚀 Deployment

### Backend (Railway/Render)
```bash
# Set environment variables
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...
```

### Frontend (Vercel)
```bash
# Set environment variable
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Test API
python main.py
# Visit http://localhost:8000/docs
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📄 License

MIT License - Free for educational and commercial use

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Pakistani e-commerce sites for data
- FastAPI, Next.js, Scrapy communities

---

**Built with ❤️ for Pakistani students**

Need help? Check `COMPLETE_SETUP_GUIDE.md` or open an issue!
