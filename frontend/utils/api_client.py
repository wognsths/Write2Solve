import requests
import os
import json
import streamlit as st
from typing import Dict, Any, Optional
import uuid
from datetime import datetime

# Docker Compose 환경에서는 컨테이너 이름으로 접근
API_BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000/api/v1")

# 오프라인 테스트 모드 (기본값: False - Docker 환경에서는 실제 API 사용)
OFFLINE_MODE = False if os.getenv("OFFLINE_MODE", "false").lower() == "false" else True

def ocr_process(image_file) -> Optional[Dict[str, Any]]:
    """
    Send image to OCR API for processing
    
    Args:
        image_file: Uploaded image file
        
    Returns:
        API response with LaTeX and rendered representation, or None if failed
    """
    # 오프라인 모드인 경우 더미 응답 반환
    if OFFLINE_MODE:
        st.warning("오프라인 모드로 실행 중입니다. 백엔드 연결 없이 테스트 데이터가 표시됩니다.")
        return {
            "id": str(uuid.uuid4()),
            "latex": "x^2 + 2x + 1 = 0",
            "rendered_latex": "x^2 + 2x + 1 = 0"
        }
        
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

def update_latex(equation_id: str, corrected_latex: str) -> Optional[Dict[str, Any]]:
    """
    Update LaTeX with corrected version
    
    Args:
        equation_id: ID of the equation to update
        corrected_latex: User-corrected LaTeX
        
    Returns:
        API response with updated rendering, or None if failed
    """
    # 오프라인 모드인 경우 더미 응답 반환
    if OFFLINE_MODE:
        return {
            "id": equation_id,
            "latex": corrected_latex,
            "rendered_latex": corrected_latex
        }
        
    try:
        data = {
            "latex": corrected_latex
        }
        
        response = requests.put(
            f"{API_BASE_URL}/equations/{equation_id}",
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
    # 오프라인 모드인 경우 더미 응답 반환
    if OFFLINE_MODE:
        if "x^2" in latex and solution.strip() in ["-1", "x=-1", "x = -1"]:
            return {
                "is_correct": True,
                "explanation": "정답입니다! x^2 + 2x + 1 = 0 방정식을 풀면 x = -1이 됩니다.",
                "step_by_step": "x^2 + 2x + 1 = 0\n(x + 1)^2 = 0\nx = -1"
            }
        return {
            "is_correct": False,
            "explanation": "오답입니다. 다시 시도해보세요.",
            "step_by_step": "x^2 + 2x + 1 = 0\n(x + 1)^2 = 0\nx = -1"
        }
        
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
