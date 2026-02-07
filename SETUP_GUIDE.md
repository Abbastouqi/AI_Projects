# Setup Guide

## Prerequisites
- Python 3.9+
- Node.js 18+
- OpenAI API Key

## Quick Start

### 1. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Create `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
CHROMA_PERSIST_DIR=./chroma_db
PORT=8000
```

Initialize vector database:
```bash
python services/vector_store.py
```

Run backend:
```bash
python main.py
```

Backend will run at: http://localhost:8000

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at: http://localhost:3000

### 3. Data Scraping (Optional)

```bash
cd scraper
pip install -r requirements.txt
python scrape_laptops.py
```

This will update `data/laptops.json` with fresh data.

## Usage

1. Open http://localhost:3000
2. Chat with the bot about your laptop needs
3. Provide your field (FSC, programming, etc.) and budget
4. Get AI-powered recommendations

## Project Structure

```
├── backend/
│   ├── api/              # API routes
│   ├── core/             # Configuration
│   ├── models/           # Data schemas
│   ├── services/         # RAG & vector store
│   └── main.py           # FastAPI app
├── frontend/
│   ├── app/              # Next.js pages
│   ├── components/       # React components
│   └── package.json
├── scraper/
│   └── scrape_laptops.py # Web scraper
└── data/
    └── laptops.json      # Laptop database
```

## Troubleshooting

**ChromaDB Error**: Delete `chroma_db` folder and re-run `python services/vector_store.py`

**CORS Error**: Ensure backend is running on port 8000

**OpenAI Error**: Check your API key in `.env` file
