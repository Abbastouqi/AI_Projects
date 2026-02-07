from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.database import get_db
from models.schemas import (
    LaptopResponse, LaptopCreate, LaptopUpdate, LaptopSearchParams,
    RecommendationResponse
)
from services.laptop_service import LaptopService, RecommendationService

laptop_router = APIRouter(prefix="/laptops", tags=["laptops"])

@laptop_router.get("/", response_model=List[LaptopResponse])
def get_laptops(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all laptops with pagination"""
    laptops = LaptopService.get_laptops(db, skip=skip, limit=limit)
    return laptops

@laptop_router.get("/{laptop_id}", response_model=LaptopResponse)
def get_laptop(laptop_id: int, db: Session = Depends(get_db)):
    """Get laptop by ID"""
    laptop = LaptopService.get_laptop(db, laptop_id)
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return laptop

@laptop_router.post("/", response_model=LaptopResponse)
def create_laptop(laptop: LaptopCreate, db: Session = Depends(get_db)):
    """Create a new laptop entry"""
    return LaptopService.create_laptop(db, laptop)

@laptop_router.put("/{laptop_id}", response_model=LaptopResponse)
def update_laptop(
    laptop_id: int,
    laptop_update: LaptopUpdate,
    db: Session = Depends(get_db)
):
    """Update laptop details"""
    laptop = LaptopService.update_laptop(db, laptop_id, laptop_update)
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return laptop

@laptop_router.delete("/{laptop_id}")
def delete_laptop(laptop_id: int, db: Session = Depends(get_db)):
    """Delete a laptop"""
    success = LaptopService.delete_laptop(db, laptop_id)
    if not success:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return {"message": "Laptop deleted successfully"}

@laptop_router.post("/search", response_model=List[LaptopResponse])
def search_laptops(params: LaptopSearchParams, db: Session = Depends(get_db)):
    """Search laptops with filters"""
    return LaptopService.search_laptops(db, params)

@laptop_router.get("/budget/{min_price}/{max_price}", response_model=List[LaptopResponse])
def get_laptops_by_budget(
    min_price: int,
    max_price: int,
    db: Session = Depends(get_db)
):
    """Get laptops within budget range"""
    return LaptopService.get_laptops_by_budget(db, min_price, max_price)

@laptop_router.get("/category/{category}", response_model=List[LaptopResponse])
def get_laptops_by_category(
    category: str,
    max_price: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get laptops for specific category (FSC Student, Programming, etc.)"""
    return LaptopService.get_laptops_for_category(db, category, max_price)

@laptop_router.get("/popular/top", response_model=List[dict])
def get_popular_laptops(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get most recommended laptops"""
    results = RecommendationService.get_popular_laptops(db, limit)
    return [
        {
            "laptop": LaptopResponse.from_orm(laptop),
            "recommendation_count": count
        }
        for laptop, count in results
    ]
