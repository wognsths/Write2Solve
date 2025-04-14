from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import logging
import shutil
import tempfile
from typing import Dict
from .ocr_service import OCRService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="OCR Service API", description="API for handwritten math OCR service")

# Initialize OCR service
ocr_service = OCRService()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "ocr"}

@app.post("/process")
async def process_image(file: UploadFile = File(...)) -> Dict[str, str]:
    """
    Process an image containing handwritten math equations
    
    Returns:
        Dictionary with LaTeX representation of the equation
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        # Copy the uploaded file to the temporary file
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
    
    try:
        # Process the image
        logger.info(f"Processing image: {file.filename}")
        latex_text = ocr_service.process_image(temp_path)
        
        # Return the result
        return {
            "latex": latex_text,
            "filename": file.filename
        }
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path) 