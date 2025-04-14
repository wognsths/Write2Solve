from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class EquationBase(BaseModel):
    """Base Equation model"""
    latex: str
    
class EquationCreate(EquationBase):
    """Model for creating a new equation"""
    image_path: Optional[str] = None

class EquationResponse(EquationBase):
    """Response model for equations"""
    rendered_latex: str
    
class EquationInDB(EquationBase):
    """Database model for equations"""
    id: str
    image_path: str
    user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
