import requests
import os
import json
import streamlit as st
from typing import Dict, Any, Optional

# API base URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

def ocr_process(image_file) -> Optional[Dict[str, Any]]:
    """
    Send image to OCR API for processing
    
    Args:
        image_file: Uploaded image file
        
    Returns:
        API response with LaTeX and rendered representation, or None if failed
    """
    try:
        files = {"file": image_file}
        response = requests.post(f"{API_BASE_URL}/ocr/", files=files)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.error(f"Error calling OCR API: {str(e)}")
        return None

def update_latex(original_latex: str, corrected_latex: str) -> Optional[Dict[str, Any]]:
    """
    Update LaTeX with corrected version
    
    Args:
        original_latex: Original LaTeX from OCR
        corrected_latex: User-corrected LaTeX
        
    Returns:
        API response with updated rendering, or None if failed
    """
    try:
        data = {
            "original_latex": original_latex,
            "corrected_latex": corrected_latex
        }
        
        response = requests.post(
            f"{API_BASE_URL}/ocr/correct/",
            data=data
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.error(f"Error calling LaTeX update API: {str(e)}")
        return None

def verify_solution(latex: str, solution: str) -> Optional[Dict[str, Any]]:
    """
    Verify solution for given equation
    
    Args:
        latex: LaTeX representation of the equation
        solution: User's solution
        
    Returns:
        API response with verification result, or None if failed
    """
    try:
        data = {
            "latex": latex,
            "solution": solution
        }
        
        response = requests.post(
            f"{API_BASE_URL}/verify/",
            json=data
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.error(f"Error calling verification API: {str(e)}")
        return None
