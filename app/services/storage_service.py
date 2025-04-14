import os
import json
import uuid
import shutil
from datetime import datetime
from pathlib import Path
import logging

class StorageService:
    """Store images, equations, and solutions"""
    
    def __init__(self):
        self.data_dir = Path("./data")
        self.images_dir = self.data_dir / "images"
        self.equations_dir = self.data_dir / "equations"
        self.solutions_dir = self.data_dir / "solutions"
        
        # Create necessary directories
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.equations_dir.mkdir(parents=True, exist_ok=True)
        self.solutions_dir.mkdir(parents=True, exist_ok=True)
    
    def save_image(self, temp_image_path: str) -> str:
        """
        Save image and return unique ID
        
        Args:
            temp_image_path: Temporary image file path
            
        Returns:
            Unique ID of saved image
        """
        # Generate unique ID
        image_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{image_id}_{timestamp}.png"
        
        # Save image
        target_path = self.images_dir / filename
        shutil.copy(temp_image_path, target_path)
        
        # Save metadata
        metadata = {
            "id": image_id,
            "filename": filename,
            "original_path": temp_image_path,
            "timestamp": timestamp
        }
        
        with open(self.images_dir / f"{image_id}_meta.json", "w") as f:
            json.dump(metadata, f, indent=2)
            
        logging.info(f"Image saved: {image_id}")
        
        return image_id
    
    def save_equation(self, image_id: str, latex: str, rendered_latex: str) -> str:
        """
        Save equation and return ID
        
        Args:
            image_id: Related image ID
            latex: Recognized LaTeX text
            rendered_latex: Rendered LaTeX
            
        Returns:
            ID of saved equation (same as image ID)
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        equation_data = {
            "id": image_id,
            "image_id": image_id,
            "latex": latex,
            "rendered_latex": rendered_latex,
            "timestamp": timestamp,
            "last_modified": timestamp
        }
        
        # Save equation
        with open(self.equations_dir / f"{image_id}.json", "w") as f:
            json.dump(equation_data, f, indent=2)
            
        logging.info(f"Equation saved: {image_id}")
        
        return image_id
    
    def update_equation(self, equation_id: str, latex: str, rendered_latex: str) -> bool:
        """
        Update existing equation
        
        Args:
            equation_id: Equation ID
            latex: Modified LaTeX text
            rendered_latex: Rendered LaTeX
            
        Returns:
            Success or failure
        """
        equation_path = self.equations_dir / f"{equation_id}.json"
        
        if not equation_path.exists():
            logging.error(f"Equation not found: {equation_id}")
            return False
            
        try:
            # Load existing data
            with open(equation_path, "r") as f:
                equation_data = json.load(f)
                
            # Update data
            equation_data["latex"] = latex
            equation_data["rendered_latex"] = rendered_latex
            equation_data["last_modified"] = datetime.now().strftime("%Y%m%d%H%M%S")
            
            # Save
            with open(equation_path, "w") as f:
                json.dump(equation_data, f, indent=2)
                
            logging.info(f"Equation updated: {equation_id}")
            return True
            
        except Exception as e:
            logging.error(f"Equation update failed: {str(e)}")
            return False
    
    def save_solution(self, equation_id: str, solution: str, is_correct: bool = None, explanation: str = None) -> str:
        """
        Save solution
        
        Args:
            equation_id: Equation ID
            solution: Solution text
            is_correct: Whether the solution is correct
            explanation: Explanation
            
        Returns:
            ID of saved solution
        """
        solution_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        solution_data = {
            "id": solution_id,
            "equation_id": equation_id,
            "solution": solution,
            "is_correct": is_correct,
            "explanation": explanation,
            "timestamp": timestamp
        }
        
        # Save solution
        with open(self.solutions_dir / f"{solution_id}.json", "w") as f:
            json.dump(solution_data, f, indent=2)
            
        logging.info(f"Solution saved: {solution_id} (equation ID: {equation_id})")
        
        return solution_id
