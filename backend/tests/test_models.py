"""
Unit tests for database models
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base, Laptop, UserSession, Recommendation
from datetime import datetime

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_laptop(db):
    """Test creating a laptop"""
    laptop = Laptop(
        brand="HP",
        model="Test Model",
        cpu="Intel i5",
        ram_gb=8,
        storage_gb=512,
        storage_type="SSD",
        gpu="Intel UHD",
        display_size=15.6,
        price_pkr=100000,
        battery_hours=6.5,
        weight_kg=1.7,
        ideal_for=["Programming", "FSC Student"]
    )
    db.add(laptop)
    db.commit()
    
    assert laptop.id is not None
    assert laptop.brand == "HP"
    assert laptop.price_pkr == 100000
    assert "Programming" in laptop.ideal_for

def test_create_user_session(db):
    """Test creating a user session"""
    session = UserSession(
        session_id="test-session-123",
        conversation_history=[{"role": "user", "content": "Hello"}],
        preferences={"budget": 100000}
    )
    db.add(session)
    db.commit()
    
    assert session.session_id == "test-session-123"
    assert len(session.conversation_history) == 1
    assert session.preferences["budget"] == 100000

def test_create_recommendation(db):
    """Test creating a recommendation"""
    # Create laptop
    laptop = Laptop(
        brand="Dell",
        model="Test",
        cpu="Intel i5",
        ram_gb=8,
        storage_gb=512,
        storage_type="SSD",
        gpu="Intel",
        display_size=15.6,
        price_pkr=100000,
        ideal_for=["Programming"]
    )
    db.add(laptop)
    
    # Create session
    session = UserSession(
        session_id="test-session",
        conversation_history=[],
        preferences={}
    )
    db.add(session)
    db.commit()
    
    # Create recommendation
    recommendation = Recommendation(
        session_id=session.session_id,
        laptop_id=laptop.id,
        rank=1,
        reason_generated="Great for programming",
        clicked=False
    )
    db.add(recommendation)
    db.commit()
    
    assert recommendation.id is not None
    assert recommendation.rank == 1
    assert recommendation.clicked is False
    assert recommendation.laptop.brand == "Dell"
    assert recommendation.session.session_id == "test-session"

def test_laptop_relationships(db):
    """Test laptop-recommendation relationships"""
    laptop = Laptop(
        brand="Lenovo",
        model="Test",
        cpu="Intel i5",
        ram_gb=8,
        storage_gb=512,
        storage_type="SSD",
        gpu="Intel",
        display_size=15.6,
        price_pkr=100000,
        ideal_for=["Programming"]
    )
    db.add(laptop)
    
    session = UserSession(session_id="test", conversation_history=[], preferences={})
    db.add(session)
    db.commit()
    
    # Add multiple recommendations
    for i in range(3):
        rec = Recommendation(
            session_id=session.session_id,
            laptop_id=laptop.id,
            rank=i+1
        )
        db.add(rec)
    db.commit()
    
    # Test relationships
    assert len(laptop.recommendations) == 3
    assert len(session.recommendations) == 3

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
