from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/knowledge/{topic}", tags=["Knowledge"])
async def get_knowledge(topic: str):
    """
    Retrieve knowledge base for a specific math topic
    """
    # Mock response for testing
    knowledge_base = {
        "quadratic_equations": {
            "formula": "x = (-b ± √(b² - 4ac)) / 2a",
            "description": "The quadratic formula is used to solve quadratic equations of the form ax² + bx + c = 0"
        },
        "derivatives": {
            "formula": "f'(x) = lim(h→0) [f(x+h) - f(x)] / h",
            "description": "The derivative measures the rate of change of a function with respect to a variable"
        }
    }
    
    if topic in knowledge_base:
        return knowledge_base[topic]
    else:
        raise HTTPException(status_code=404, detail=f"Knowledge for {topic} not found")
