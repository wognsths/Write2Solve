import os
import uuid
import base64
import json
from pathlib import Path
import requests

from dotenv import load_dotenv
load_dotenv()

# Create directories for saving images and LaTeX data (only runs once)
IMAGE_DIR = Path("./data/local/images")
LATEX_DIR = Path("./data/local/math_expressions")

IMAGE_DIR.mkdir(parents=True, exist_ok=True)
LATEX_DIR.mkdir(parents=True, exist_ok=True)

def process_image(image_base64):
    """
    Process an image using Mathpix API and save the results locally.
    
    Args:
        image_base64 (str): Base64-encoded image data
    
    Returns:
        dict: JSON data containing the image ID and LaTeX expression
    """
    # Generate a unique ID for the image and LaTeX data
    file_id = str(uuid.uuid4())
    
    try:
        # 1. Decode the Base64 image data and save it as a PNG file
        image_data = base64.b64decode(image_base64)
        image_path = IMAGE_DIR / f"{file_id}.png"
        with open(image_path, "wb") as f:
            f.write(image_data)
        
        # 2. Send a request to the Mathpix API for OCR processing
        headers = {
            "app_id": os.getenv("MATHPIX_API_ID"),  # Replace with your Mathpix App ID
            "app_key": os.getenv("MATHPIX_API_KEY"),  # Replace with your Mathpix App Key
            "Content-type": "application/json"
        }
        payload = {
            "src": f"data:image/jpeg;base64,{image_base64}",
            "formats": ["latex_styled"]
        }
        response = requests.post("https://api.mathpix.com/v3/text", json=payload, headers=headers)
        
        # Check if the API call was successful
        if response.status_code != 200:
            raise Exception(f"Mathpix API call failed: {response.text}")
        
        # 3. Save the LaTeX result as a JSON file
        latex_result = response.json().get("latex_styled")
        latex_data = {
            "id": file_id,  # Use the same ID as the image file
            "latex_expression": latex_result
        }
        latex_path = LATEX_DIR / f"{file_id}.json"
        with open(latex_path, "w", encoding="utf-8") as f:
            json.dump(latex_data, f, ensure_ascii=False, indent=4)  # Serialize JSON
        
        return latex_data
    
    except Exception as e:
        # If an error occurs, delete any partially saved files
        if 'image_path' in locals() and os.path.exists(image_path):
            os.remove(image_path)
        if 'latex_path' in locals() and os.path.exists(latex_path):
            os.remove(latex_path)
        raise e