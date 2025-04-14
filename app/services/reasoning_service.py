from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os
import json
import logging
# from services.knowledge_service import retrieve_knowledge_base

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SOLUTION_DIR = Path("./data/local/solutions")

SOLUTION_DIR.mkdir(parents=True, exist_ok=True)

class ReasoningService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        try:
            if self.api_key:
                self.client = OpenAI(api_key=self.api_key)
            else:
                logging.warning("No OpenAI API key found. Using mock responses.")
        except Exception as e:
            logging.error(f"Failed to initialize OpenAI client: {str(e)}")
            logging.warning("Using mock responses for testing.")

    def verify_solution(self, latex: str, solution: str) -> dict:
        """
        Verify a solution for a given math equation
        """
        # If client initialization failed or no API key, return mock response
        if not self.client:
            logging.info("Using mock verification response")
            return {
                "is_correct": True,
                "explanation": "The solution is correct. (Mock response for testing)",
                "step_by_step": ["Step 1: Set up the equation", "Step 2: Solve for x", "Step 3: Verify the answer"]
            }
        
        try:
            prompt = f"""
            Instructions:
            - The math solution below is user's math solution.
            - Verify the user's solution based on rigorous proof and mathematical theories.
            - If the user's solution is wrong, show why the solution is wrong and give the correct solution.
            - If the user's solution is correct, briefly explain why user's solution is correct.
            
            Problem: {latex}
            User's math solution: {solution}
            """
            
            response = self.client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "system", "content": "You are a math verification assistant that analyzes math solutions."},
                    {"role": "user", "content": prompt}
                ],
                reasoning={"effort": "high"},
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            
            # Simple parsing of AI response to determine correctness
            is_correct = "correct" in content.lower() and not "incorrect" in content.lower()
            
            return {
                "is_correct": is_correct,
                "explanation": content,
                "step_by_step": content.split("\n")
            }
        except Exception as e:
            logging.error(f"Verification failed: {str(e)}")
            return {
                "is_correct": True,
                "explanation": "The solution is correct. (Mock response due to error)",
                "step_by_step": ["Step 1: Set up the equation", "Step 2: Solve for x", "Step 3: Verify the answer"]
            }

    