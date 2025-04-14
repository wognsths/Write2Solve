import streamlit as st
import base64
from IPython.display import Math, display
import matplotlib.pyplot as plt
import io

def display_equation(rendered_latex: str):
    """
    Display a rendered LaTeX equation in Streamlit
    
    Args:
        rendered_latex: HTML representation of rendered LaTeX
    """
    # Display using HTML
    st.markdown(rendered_latex, unsafe_allow_html=True)
    
    # Add MathJax support
    st.markdown(
        """
        <script type="text/javascript" async
            src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
        </script>
        """,
        unsafe_allow_html=True
    )
