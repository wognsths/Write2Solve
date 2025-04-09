from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os
import json
from services.knowledge_service import retrieve_knowledge_base

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SOLUTION_DIR = Path("./data/local/solutions")

SOLUTION_DIR.mkdir(parents=True, exist_ok=True)

client = OpenAI(api_key=OPENAI_API_KEY)

def verify_solution(latex_data: dict) -> str:
    latex_expr = latex_data["latex_expression"]
    knowledge_base = retrieve_knowledge_base(latex_data["latex_expression"])

    prompt=f"""
Instructions:
- The math solution below is user's math solution.
- Verify the user's solution based on rigorous proof and mathematical theories.
- If the user's solution is wrong, show why the solution is wrong and give the correct solution.
- If the user's solution is correct, briefly explain why user's solution is correct.
- You have access to the following knowledge base:
{knowledge_base}

User's math solution: {latex_expr}
"""
    
    try:
        response = client.responses.create(
            model="o3-mini",
            reasoning={"effort": "medium"},
            input=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        if response.status == "completed":
            output_text = response.output_text
            
            result = {
                "id": latex_data["id"],
                "problem": latex_expr,
                "verification": output_text,
                "tokens_used": response.usage.total_tokens
            }
            
            # Save as JSON
            file_path = SOLUTION_DIR / f"{latex_data['id']}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            return output_text
        
        else:
            raise RuntimeError(f"Response failed with status: {response.status}")
            
    except Exception as e:
        error_msg = f"Verification failed: {str(e)}"
        error_result = {
            "id": latex_data["id"],
            "error": error_msg
        }
        
        error_path = SOLUTION_DIR / f"{latex_data['id']}_error.json"
        with open(error_path, 'w', encoding='utf-8') as f:
            json.dump(error_result, f, ensure_ascii=False, indent=2)
        
        return error_msg

    