from fastapi import FastAPI
from app.routes import ocr, verify, knowledge
import os
from pathlib import Path
import requests
from fastapi import HTTPException

app = FastAPI()

app.include_router(ocr.router, tags=["OCR"])
app.include_router(verify.router, tags=["Verification"])
app.include_router(knowledge.router, tags=["Knowledge"])

MATHPIX_API_ID = os.getenv("MATHPIX_API_ID")
MATHPIX_API_KEY = os.getenv("MATHPIX_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not MATHPIX_API_ID:
    raise ValueError("MATHPIX_API_ID environment variable is not set")
if not MATHPIX_API_KEY:
    raise ValueError("MATHPIX_API_KEY environment variable is not set")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "local"

@app.get("/")
def read_root():
    try:
        response = requests.get("https://api.mathpix.com/v3/health")
        if response.status_code == 200:
            return {
                "message": "Handwritten Math Solution Checker API",
                "status": "healthy",
                "mathpix_api": "available"
            }
        else:
            return {
                "message": "Handwritten Math Solution Checker API",
                "status": "warning",
                "mathpix_api": "unavailable"
            }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)