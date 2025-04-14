from fastapi import APIRouter, HTTPException, Body
from services.reasoning_service import ReasoningService
from models.solution import SolutionRequest, SolutionResponse

router = APIRouter()
reasoning_service = ReasoningService()

@router.post("/verify/", response_model=SolutionResponse)
async def verify_solution(request: SolutionRequest = Body(...)):
    """
    Verify a solution for a given math equation
    """
    try:
        # Process solution using reasoning service
        verification_result = reasoning_service.verify_solution(
            request.latex,
            request.solution
        )
        
        return {
            "is_correct": verification_result["is_correct"],
            "explanation": verification_result["explanation"],
            "step_by_step": verification_result["step_by_step"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")
