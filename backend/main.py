from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

from api.routes import chat_router
from api.laptop_routes import laptop_router
from core.config import settings
from models.database import init_db

load_dotenv()

# Initialize database on startup
init_db()

app = FastAPI(title="Laptop Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for HTML file access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")
app.include_router(laptop_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Laptop Recommendation API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
