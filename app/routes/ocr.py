from fastapi import APIRouter, HTTPException
from app.services.mathpix_service import process_image

router = APIRouter()

@router.post("/process")
async def process_ocr(image_base64: str):
    try:
        result = process_image(image_base64)
        return {"latex": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))