from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models.database import Laptop, UserSession, Recommendation
from models.schemas import LaptopCreate, LaptopUpdate, LaptopSearchParams
from typing import List, Optional

class LaptopService:
    """Service layer for laptop operations"""
    
    @staticmethod
    def create_laptop(db: Session, laptop: LaptopCreate) -> Laptop:
        """Create a new laptop entry"""
        db_laptop = Laptop(**laptop.dict())
        db.add(db_laptop)
        db.commit()
        db.refresh(db_laptop)
        return db_laptop
    
    @staticmethod
    def get_laptop(db: Session, laptop_id: int) -> Optional[Laptop]:
        """Get laptop by ID"""
        return db.query(Laptop).filter(Laptop.id == laptop_id).first()
    
    @staticmethod
    def get_laptops(db: Session, skip: int = 0, limit: int = 100) -> List[Laptop]:
        """Get all laptops with pagination"""
        return db.query(Laptop).offset(skip).limit(limit).all()
    
    @staticmethod
    def search_laptops(db: Session, params: LaptopSearchParams) -> List[Laptop]:
        """Search laptops with filters"""
        query = db.query(Laptop)
        
        if params.brand:
            query = query.filter(Laptop.brand.ilike(f"%{params.brand}%"))
        
        if params.min_price is not None:
            query = query.filter(Laptop.price_pkr >= params.min_price)
        
        if params.max_price is not None:
            query = query.filter(Laptop.price_pkr <= params.max_price)
        
        if params.min_ram is not None:
            query = query.filter(Laptop.ram_gb >= params.min_ram)
        
        if params.storage_type:
            query = query.filter(Laptop.storage_type == params.storage_type)
        
        if params.ideal_for:
            # Search in JSON array
            query = query.filter(Laptop.ideal_for.contains([params.ideal_for]))
        
        return query.all()
    
    @staticmethod
    def update_laptop(db: Session, laptop_id: int, laptop_update: LaptopUpdate) -> Optional[Laptop]:
        """Update laptop details"""
        db_laptop = db.query(Laptop).filter(Laptop.id == laptop_id).first()
        if not db_laptop:
            return None
        
        update_data = laptop_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_laptop, field, value)
        
        db.commit()
        db.refresh(db_laptop)
        return db_laptop
    
    @staticmethod
    def delete_laptop(db: Session, laptop_id: int) -> bool:
        """Delete a laptop"""
        db_laptop = db.query(Laptop).filter(Laptop.id == laptop_id).first()
        if not db_laptop:
            return False
        
        db.delete(db_laptop)
        db.commit()
        return True
    
    @staticmethod
    def get_laptops_by_budget(db: Session, min_price: int, max_price: int) -> List[Laptop]:
        """Get laptops within budget range"""
        return db.query(Laptop).filter(
            and_(Laptop.price_pkr >= min_price, Laptop.price_pkr <= max_price)
        ).order_by(Laptop.price_pkr).all()
    
    @staticmethod
    def get_laptops_for_category(db: Session, category: str, max_price: Optional[int] = None) -> List[Laptop]:
        """Get laptops suitable for a specific category"""
        query = db.query(Laptop).filter(Laptop.ideal_for.contains([category]))
        
        if max_price:
            query = query.filter(Laptop.price_pkr <= max_price)
        
        return query.order_by(Laptop.price_pkr).all()

class SessionService:
    """Service layer for user session operations"""
    
    @staticmethod
    def create_session(db: Session, session_id: str) -> UserSession:
        """Create a new user session"""
        db_session = UserSession(
            session_id=session_id,
            conversation_history=[],
            preferences={}
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session
    
    @staticmethod
    def get_session(db: Session, session_id: str) -> Optional[UserSession]:
        """Get session by ID"""
        return db.query(UserSession).filter(UserSession.session_id == session_id).first()
    
    @staticmethod
    def get_or_create_session(db: Session, session_id: str) -> UserSession:
        """Get existing session or create new one"""
        session = SessionService.get_session(db, session_id)
        if not session:
            session = SessionService.create_session(db, session_id)
        return session
    
    @staticmethod
    def update_conversation(db: Session, session_id: str, message: dict) -> UserSession:
        """Add message to conversation history"""
        session = SessionService.get_or_create_session(db, session_id)
        session.conversation_history.append(message)
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def update_preferences(db: Session, session_id: str, preferences: dict) -> UserSession:
        """Update user preferences"""
        session = SessionService.get_or_create_session(db, session_id)
        session.preferences.update(preferences)
        db.commit()
        db.refresh(session)
        return session

class RecommendationService:
    """Service layer for recommendation operations"""
    
    @staticmethod
    def create_recommendation(
        db: Session,
        session_id: str,
        laptop_id: int,
        rank: int,
        reason: Optional[str] = None
    ) -> Recommendation:
        """Create a new recommendation"""
        db_recommendation = Recommendation(
            session_id=session_id,
            laptop_id=laptop_id,
            rank=rank,
            reason_generated=reason,
            clicked=False
        )
        db.add(db_recommendation)
        db.commit()
        db.refresh(db_recommendation)
        return db_recommendation
    
    @staticmethod
    def mark_clicked(db: Session, recommendation_id: int) -> Optional[Recommendation]:
        """Mark recommendation as clicked"""
        recommendation = db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
        if recommendation:
            recommendation.clicked = True
            db.commit()
            db.refresh(recommendation)
        return recommendation
    
    @staticmethod
    def get_session_recommendations(db: Session, session_id: str) -> List[Recommendation]:
        """Get all recommendations for a session"""
        return db.query(Recommendation).filter(
            Recommendation.session_id == session_id
        ).order_by(Recommendation.created_at.desc()).all()
    
    @staticmethod
    def get_popular_laptops(db: Session, limit: int = 10) -> List[tuple]:
        """Get most recommended laptops"""
        from sqlalchemy import func
        
        results = db.query(
            Laptop,
            func.count(Recommendation.id).label('recommendation_count')
        ).join(
            Recommendation, Laptop.id == Recommendation.laptop_id
        ).group_by(
            Laptop.id
        ).order_by(
            func.count(Recommendation.id).desc()
        ).limit(limit).all()
        
        return results
