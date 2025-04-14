from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
import shutil
import os
from tempfile import NamedTemporaryFile
from app.services.ocr_service import OCRService
from app.services.latex_service import LaTeXService
from app.models.equation import EquationCreate, EquationResponse

router = APIRouter()
ocr_service = OCRService()
latex_service = LaTeXService()

@router.post("/ocr/", response_model=EquationResponse)
async def process_image(file: UploadFile = File(...)):
    """
    Process an image containing handwritten math equations and convert to LaTeX
    """
    try:
        # Save uploaded file to a temporary file
        with NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name
        
        # Process image with OCR service
        latex_text = ocr_service.process_image(temp_file_path)
        
        # Render to user-friendly format
        rendered_latex = latex_service.render(latex_text)
        
        # Remove temporary file
        os.unlink(temp_file_path)
        
        return {
            "latex": latex_text,
            "rendered_latex": rendered_latex
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

@router.post("/ocr/correct/", response_model=EquationResponse)
async def correct_ocr(
    equation_id: Optional[str] = Form(None),
    original_latex: str = Form(...),
    corrected_latex: str = Form(...)
):
    """
    Save a correction to the OCR result for model improvement
    """
    # Store correction for model retraining
    ocr_service.save_correction(original_latex, corrected_latex)
    
    # Render corrected LaTeX for display
    rendered_latex = latex_service.render(corrected_latex)
    
    return {
        "latex": corrected_latex,
        "rendered_latex": rendered_latex
    }
