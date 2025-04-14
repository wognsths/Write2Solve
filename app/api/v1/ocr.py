from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
import shutil
import os
from tempfile import NamedTemporaryFile
from services.ocr_service import OCRService
from services.latex_service import LaTeXService
from services.storage_service import StorageService
from models.equation import EquationCreate, EquationResponse
import json
from services.reasoning_service import ReasoningService
from models.solution import SolutionResponse

router = APIRouter()
ocr_service = OCRService()
latex_service = LaTeXService()
storage_service = StorageService()
reasoning_service = ReasoningService()

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
        
        # 이미지 저장하고 ID 얻기
        image_id = storage_service.save_image(temp_file_path)
        
        # Process image with OCR service
        latex_text = ocr_service.process_image(temp_file_path)
        
        # Validate the LaTeX syntax
        is_valid = latex_service.validate(latex_text)
        
        if not is_valid:
            raise HTTPException(status_code=422, detail="Generated LaTeX is invalid")
        
        # Render the LaTeX for display
        rendered_latex = latex_service.render(latex_text)
        
        # save equation
        equation_id = storage_service.save_equation(image_id, latex_text, rendered_latex)
        
        # Create response
        response = EquationResponse(
            id=equation_id,
            latex=latex_text,
            rendered_latex=rendered_latex
        )
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        return response
    
    except Exception as e:
        # Make sure to clean up the temp file in case of errors
        if 'temp_file_path' in locals():
            os.unlink(temp_file_path)
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

@router.put("/equations/{equation_id}", response_model=EquationResponse)
async def update_equation(equation_id: str, latex: str = Form(...)):
    """
    Update an existing equation with corrected LaTeX
    """
    try:
        # 새로운 LaTeX 렌더링
        rendered_latex = latex_service.render(latex)
        
        # 수식 업데이트
        success = storage_service.update_equation(equation_id, latex, rendered_latex)
        
        if not success:
            raise HTTPException(status_code=404, detail="Equation not found")
        
        # 응답 생성
        response = EquationResponse(
            id=equation_id,
            latex=latex,
            rendered_latex=rendered_latex
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update equation: {str(e)}")

@router.post("/solutions/", response_model=SolutionResponse)
async def save_solution(equation_id: str = Form(...), solution: str = Form(...)):
    """
    Save a solution for an equation and verify if it's correct
    """
    try:
        # 저장된 수식 가져오기
        equation_path = os.path.join(storage_service.equations_dir, f"{equation_id}.json")
        if not os.path.exists(equation_path):
            raise HTTPException(status_code=404, detail="Equation not found")
            
        with open(equation_path, "r") as f:
            equation_data = json.load(f)
            
        latex = equation_data["latex"]
        
        # 솔루션 검증
        verification_result = reasoning_service.verify_solution(latex, solution)
        
        # 솔루션 저장
        solution_id = storage_service.save_solution(
            equation_id=equation_id,
            solution=solution,
            is_correct=verification_result["is_correct"],
            explanation=verification_result["explanation"]
        )
        
        return {
            "is_correct": verification_result["is_correct"],
            "explanation": verification_result["explanation"],
            "step_by_step": verification_result["step_by_step"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save solution: {str(e)}")

@router.get("/equations/{equation_id}", response_model=EquationResponse)
async def get_equation(equation_id: str):
    """
    Get the equation by ID
    """
    try:
        equation_path = os.path.join(storage_service.equations_dir, f"{equation_id}.json")
        if not os.path.exists(equation_path):
            raise HTTPException(status_code=404, detail="Equation not found")
            
        with open(equation_path, "r") as f:
            equation_data = json.load(f)
        
        return EquationResponse(
            id=equation_id,
            latex=equation_data["latex"],
            rendered_latex=equation_data["rendered_latex"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get equation: {str(e)}")
