from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SolutionRequest(BaseModel):
    """Request model for solution verification"""
    latex: str
    solution: str

class SolutionResponse(BaseModel):
    """Response model for solution verification"""
    is_correct: bool
    explanation: str
    step_by_step: List[str]
    
class SolutionInDB(BaseModel):
    """Database model for solutions"""
    id: str
    equation_id: str
    solution_text: str
    is_correct: bool
    user_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True
