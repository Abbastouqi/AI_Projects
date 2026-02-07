# 🤖 AI-Powered Laptop Recommendation Chatbot for Pakistani Students

An intelligent chatbot that helps Pakistani students find the perfect laptop based on their needs, budget, and use case. Built with FastAPI, Next.js, and AI-powered conversation flow.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🎓 **Student-Focused**: Tailored for FSC and university students in Pakistan
- 💰 **Budget-Aware**: Recommendations based on PKR budget (50k - 250k+)
- 🎯 **Use-Case Detection**: Programming, Gaming, Office Work, Engineering, etc.
- 🇵🇰 **Local Market Integration**: Prices from Czone, Paklap, Daraz, Telemart
- 💬 **Conversational AI**: Natural language understanding with intent detection
- 🔍 **Smart Comparison**: Compare multiple laptops side-by-side
- 📊 **16+ Laptops Database**: HP, Dell, Lenovo, ASUS with real specs
- 🌐 **Web Scraping**: Automated data collection from Pakistani e-commerce sites

## 🏗️ Architecture

```
├── backend/              # FastAPI Backend
│   ├── api/             # REST API endpoints
│   ├── models/          # SQLAlchemy models & schemas
│   ├── services/        # Business logic & AI services
│   └── scripts/         # Database initialization
├── frontend/            # Next.js Frontend (React + TypeScript)
│   ├── app/            # Next.js 14 app directory
│   ├── components/     # React components
│   └── types/          # TypeScript definitions
├── scraper/            # Scrapy web scraper
│   └── scrapy_project/ # Spider implementations
├── data/               # Laptop data (JSON)
└── simple-chat.html    # Standalone HTML interface
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+ (optional, for Next.js frontend)
- pip or uv for Python packages

### 1. Clone the Repository

```bash
git clone https://github.com/Abbastouqi/AI_Projects.git
cd AI_Projects
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Create .env file (optional)
cp backend/.env.example backend/.env

# Run the backend
python backend/main.py
```

Backend will start at: **http://localhost:8000**

### 3. Start Chatting!

**Option A: Simple HTML Interface (Recommended)**
1. Open `simple-chat.html` in your browser
2. Start chatting immediately!

**Option B: API Documentation**
- Visit: http://localhost:8000/docs
- Test the `/api/chat` endpoint directly

**Option C: Next.js Frontend (Advanced)**
```bash
cd frontend
npm install
npm run dev
```
Visit: http://localhost:3000

## 💬 Example Conversations

Try these messages:

```
"Hi, I'm an FSC student looking for a laptop"
"I need a laptop for programming under 80,000 PKR"
"Show me gaming laptops"
"Compare HP and Dell laptops"
"السلام علیکم" (Urdu greeting)
"What's the best laptop for engineering students?"
```

## 🗄️ Database

The chatbot uses SQLite with 3 main tables:

1. **Laptop**: 16 pre-loaded Pakistani laptops with specs and prices
2. **UserSession**: Conversation history and user preferences
3. **Recommendation**: Tracking of recommended laptops

Initialize database:
```bash
python backend/scripts/init_database.py
```

## 🕷️ Web Scraper

Scrape laptop data from Pakistani e-commerce sites:

```bash
cd scraper/scrapy_project
python run_all_spiders.py
```

Supported sites:
- Czone.pk
- Paklap.pk
- Telemart.pk

## 🧪 Testing

Test the backend API:

```bash
python test_chat_working.py
```

Expected output:
```
✅ Backend is running!
✅ Chat endpoint is working!
✅ Laptops endpoint working! Found 16 laptops in database
🎉 ALL TESTS PASSED!
```

## 📁 Project Structure

```
backend/
├── api/
│   ├── routes.py              # Chat endpoints
│   └── laptop_routes.py       # Laptop CRUD endpoints
├── models/
│   ├── database.py            # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   └── seed_data.py           # Sample laptop data
├── services/
│   ├── conversation_manager.py    # Conversation flow logic
│   ├── laptop_service.py          # Laptop business logic
│   ├── recommendation_engine.py   # Recommendation algorithm
│   └── intent_detector.py         # Intent classification
└── main.py                    # FastAPI application

frontend/
├── components/
│   ├── ChatInterface.tsx      # Main chat UI
│   ├── MessageBubble.tsx      # Chat messages
│   ├── LaptopCard.tsx         # Laptop display cards
│   ├── QuickReplies.tsx       # Quick reply buttons
│   └── ComparisonView.tsx     # Laptop comparison
└── app/
    └── page.tsx               # Home page

scraper/
└── scrapy_project/
    └── laptop_scraper/
        ├── spiders/           # Web scrapers
        └── pipelines.py       # Data processing
```

## 🎯 Key Features Explained

### Intent Detection
The chatbot recognizes 6 types of user intents:
- Greeting
- Budget Query
- Use Case Query
- Comparison Request
- Specific Laptop Question
- Purchase Help

### Conversation Flow
1. **Greeting** → Welcome message
2. **Needs Analysis** → Ask about use case
3. **Budget Check** → Determine price range
4. **Recommendation** → Suggest laptops
5. **Comparison** → Compare selected laptops

### Recommendation Engine
Filters laptops based on:
- Budget range (PKR)
- Use case (programming, gaming, office, etc.)
- Student type (FSC, University)
- Brand preference
- Specifications (RAM, CPU, Storage)

## 🛠️ Technologies Used

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM for database
- Pydantic - Data validation
- Uvicorn - ASGI server

**Frontend:**
- Next.js 14 - React framework
- TypeScript - Type safety
- Tailwind CSS - Styling
- React Hooks - State management

**Scraper:**
- Scrapy - Web scraping framework
- BeautifulSoup - HTML parsing

## 📝 API Endpoints

### Chat Endpoints
- `POST /api/chat` - Send message and get response
- `GET /api/health` - Health check
- `GET /api/session/{session_id}` - Get conversation history

### Laptop Endpoints
- `GET /api/laptops` - Get all laptops
- `GET /api/laptops/{id}` - Get specific laptop
- `POST /api/laptops` - Add new laptop
- `PUT /api/laptops/{id}` - Update laptop
- `DELETE /api/laptops/{id}` - Delete laptop

## 🔧 Configuration

### Backend (.env)
```env
DATABASE_URL=sqlite:///./laptop_recommendations.db
PORT=8000
OPENAI_API_KEY=your_key_here  # Optional for RAG
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Abbas Touqi**
- Email: abbastouqeer399@gmail.com
- GitHub: [@Abbastouqi](https://github.com/Abbastouqi)

## 🙏 Acknowledgments

- Pakistani e-commerce sites for laptop data
- FastAPI and Next.js communities
- All contributors and users

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/Abbastouqi/AI_Projects/issues) page
2. Create a new issue with detailed description
3. Email: abbastouqeer399@gmail.com

---

⭐ If you find this project helpful, please give it a star!
