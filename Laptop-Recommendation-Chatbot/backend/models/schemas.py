from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

# Laptop Schemas
class LaptopBase(BaseModel):
    brand: str = Field(..., min_length=1, max_length=50)
    model: str = Field(..., min_length=1, max_length=100)
    cpu: str = Field(..., min_length=1, max_length=100)
    ram_gb: int = Field(..., gt=0, le=128)
    storage_gb: int = Field(..., gt=0, le=8192)
    storage_type: str = Field(..., pattern="^(SSD|HDD|Hybrid)$")
    gpu: str = Field(..., min_length=1, max_length=100)
    display_size: float = Field(..., gt=10.0, le=20.0)
    price_pkr: int = Field(..., gt=0)
    battery_hours: Optional[float] = Field(None, gt=0, le=24)
    weight_kg: Optional[float] = Field(None, gt=0, le=5)
    ideal_for: List[str] = Field(..., min_items=1)
    source_url: Optional[str] = Field(None, max_length=500)

class LaptopCreate(LaptopBase):
    pass

class LaptopUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    cpu: Optional[str] = None
    ram_gb: Optional[int] = None
    storage_gb: Optional[int] = None
    storage_type: Optional[str] = None
    gpu: Optional[str] = None
    display_size: Optional[float] = None
    price_pkr: Optional[int] = None
    battery_hours: Optional[float] = None
    weight_kg: Optional[float] = None
    ideal_for: Optional[List[str]] = None
    source_url: Optional[str] = None

class LaptopResponse(LaptopBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# UserSession Schemas
class UserSessionBase(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100)

class UserSessionCreate(UserSessionBase):
    conversation_history: Optional[List[dict]] = Field(default_factory=list)
    preferences: Optional[dict] = Field(default_factory=dict)

class UserSessionUpdate(BaseModel):
    conversation_history: Optional[List[dict]] = None
    preferences: Optional[dict] = None

class UserSessionResponse(UserSessionBase):
    conversation_history: List[dict]
    preferences: dict
    created_at: datetime
    
    class Config:
        from_attributes = True

# Recommendation Schemas
class RecommendationBase(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100)
    laptop_id: int = Field(..., gt=0)
    rank: int = Field(..., ge=1, le=10)
    reason_generated: Optional[str] = None
    clicked: bool = False

class RecommendationCreate(RecommendationBase):
    pass

class RecommendationUpdate(BaseModel):
    rank: Optional[int] = None
    reason_generated: Optional[str] = None
    clicked: Optional[bool] = None

class RecommendationResponse(RecommendationBase):
    id: int
    created_at: datetime
    laptop: Optional[LaptopResponse] = None
    
    class Config:
        from_attributes = True

# Chat Schemas (keeping existing ones)
class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    recommendations: Optional[List[LaptopResponse]] = None

# Search/Filter Schemas
class LaptopSearchParams(BaseModel):
    brand: Optional[str] = None
    min_price: Optional[int] = Field(None, ge=0)
    max_price: Optional[int] = Field(None, ge=0)
    min_ram: Optional[int] = Field(None, ge=0)
    storage_type: Optional[str] = None
    ideal_for: Optional[str] = None
    
    @validator('max_price')
    def validate_price_range(cls, v, values):
        if v is not None and 'min_price' in values and values['min_price'] is not None:
            if v < values['min_price']:
                raise ValueError('max_price must be greater than min_price')
        return v
