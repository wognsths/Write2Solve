from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import ocr, verify, knowledge

app = FastAPI(
    title="Write2Solve API",
    description="API for OCR of handwritten math equations with solutions",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ocr.router, prefix="/api/v1", tags=["OCR"])
app.include_router(verify.router, prefix="/api/v1", tags=["Verification"])
app.include_router(knowledge.router, prefix="/api/v1", tags=["Knowledge"])

@app.get("/", tags=["Health"])
async def root():
    return {"message": "Write2Solve API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
