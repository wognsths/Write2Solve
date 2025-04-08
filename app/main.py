from fastapi import FastAPI
from app.routes import ocr, verify

app = FastAPI()

app.include_router(ocr.router, prefix="/ocr", tags=["OCR"])
app.include_router(verify.router, prefix="/verify", tags=["Verification"])

@app.get("/")
def read_root():
    return {"message": "Handwritten Math Solution Checker API"}