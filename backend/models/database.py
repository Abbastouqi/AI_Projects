from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./laptop_recommendations.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency for FastAPI routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Laptop(Base):
    __tablename__ = "laptops"
    
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(50), nullable=False, index=True)
    model = Column(String(100), nullable=False)
    cpu = Column(String(100), nullable=False)
    ram_gb = Column(Integer, nullable=False)
    storage_gb = Column(Integer, nullable=False)
    storage_type = Column(String(20), nullable=False)  # SSD, HDD, Hybrid
    gpu = Column(String(100), nullable=False)
    display_size = Column(Float, nullable=False)  # in inches
    price_pkr = Column(Integer, nullable=False, index=True)
    battery_hours = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    ideal_for = Column(JSON, nullable=False)  # ["FSC Student", "Programming", "Gaming"]
    source_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    recommendations = relationship("Recommendation", back_populates="laptop")
    
    def __repr__(self):
        return f"<Laptop {self.brand} {self.model} - PKR {self.price_pkr}>"

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    session_id = Column(String(100), primary_key=True, index=True)
    conversation_history = Column(JSON, default=list)  # [{"role": "user", "content": "..."}]
    preferences = Column(JSON, default=dict)  # {"budget": 100000, "field": "programming"}
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    recommendations = relationship("Recommendation", back_populates="session")
    
    def __repr__(self):
        return f"<UserSession {self.session_id}>"

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), ForeignKey("user_sessions.session_id"), nullable=False)
    laptop_id = Column(Integer, ForeignKey("laptops.id"), nullable=False)
    rank = Column(Integer, nullable=False)  # 1, 2, 3 for top recommendations
    reason_generated = Column(Text, nullable=True)  # AI-generated explanation
    clicked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("UserSession", back_populates="recommendations")
    laptop = relationship("Laptop", back_populates="recommendations")
    
    def __repr__(self):
        return f"<Recommendation {self.session_id} -> Laptop {self.laptop_id} (Rank {self.rank})>"

def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
