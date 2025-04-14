import streamlit as st
import requests
import io
import base64
from PIL import Image
from frontend.components import upload_widget, equation_editor, latex_renderer
from frontend.utils import api_client

def show():
    st.title("Upload & Edit Equation")
    
    # Instructions
    st.write("""
    Upload a photo of your handwritten math equation. 
    The system will convert it to LaTeX format, which you can edit if needed.
    """)
    
    # Upload widget for equation image
    uploaded_file = upload_widget.image_uploader(
        label="Upload handwritten equation",
        key="equation_upload"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Equation", use_column_width=True)
        
        # Process with OCR on button click
        if st.button("Process Equation"):
            with st.spinner("Processing equation..."):
                # Reset file position
                uploaded_file.seek(0)
                
                # Call OCR API
                ocr_result = api_client.ocr_process(uploaded_file)
                
                if ocr_result:
                    # Save to session state
                    st.session_state.equation_latex = ocr_result["latex"]
                    st.session_state.rendered_latex = ocr_result["rendered_latex"]
                    
                    st.success("Equation processed successfully!")
                else:
                    st.error("Failed to process equation. Please try again.")
    
    # If we have processed LaTeX, show the editor
    if "equation_latex" in st.session_state and st.session_state.equation_latex:
        st.subheader("LaTeX Result")
        
        # Display rendered equation
        latex_renderer.display_equation(st.session_state.rendered_latex)
        
        # LaTeX editor
        edited_latex = equation_editor.latex_editor(
            initial_value=st.session_state.equation_latex,
            key="latex_editor"
        )
        
        # If edited, update the rendering
        if edited_latex != st.session_state.equation_latex:
            if st.button("Update Rendering"):
                with st.spinner("Updating..."):
                    # Call API to re-render with corrections
                    result = api_client.update_latex(
                        st.session_state.equation_latex, 
                        edited_latex
                    )
                    
                    if result:
                        st.session_state.equation_latex = edited_latex
                        st.session_state.rendered_latex = result["rendered_latex"]
                        st.success("Rendering updated!")
                    else:
                        st.error("Failed to update rendering. Please try again.")
        
        # Continue to verification
        if st.button("Continue to Solution Verification"):
            st.session_state.page = "verify"
            st.experimental_rerun()
