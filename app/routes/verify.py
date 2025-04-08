from fastapi import APIRouter, HTTPException
from app.services.llm_service import verify_solution

router = APIRouter()

@router.post("/check")
async def check_solution(solution: str):
    try:
        result = verify_solution(solution)
        return {"verification": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))