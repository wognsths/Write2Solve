import streamlit as st
import streamlit.components.v1 as components
import os
import base64
import requests
import json
from pathlib import Path

# Create directory for modified LaTeX expressions
MODIFIED_DIR = Path("./data/local/modified")
MODIFIED_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .scrollable-container {
        max-height: 300px;
        overflow-y: auto;
        padding-right: 10px; /* optional: avoids clipping scrollbar */
    }
    <style>
""", unsafe_allow_html=True)

DEBUG_MODE = False
TEST_DEBUG_MODE = False

st.title("Capture your handwritten solution, and verify it easily!")

tab1, tab2 = st.tabs(["Step 1: Capture solution", "Step 2: Validate solution"])

with tab1:
    st.header("Step 1: Capture and upload your solution")

    container = st.container()
    with container:
        status_placeholder = st.empty()

    with st.form("capture_input_form", clear_on_submit=False):
        uploaded_file = st.file_uploader(
            "Upload your captured solution", type=["png", "jpeg"]
            )
        submit_button = st.form_submit_button("Submit")

    if submit_button and uploaded_file:
        if uploaded_file:
            file_bytes = uploaded_file.read()
            base64_image = base64.b64encode(file_bytes).decode("utf-8")

            with container:
                col1, col2 = st.columns(2, gap="small")

            img_display = f"""
            <div class="image-container">
                <embed
                    src="data:application/img;base64{base64_image}"
                    width="100%"
                    height="700"
                    type="application/img">
            </div>
            """
            with col1:
                st.markdown(img_display, unsafe_allow_html=True)
        
            with col2:
                with st.spinner("Checking image...", show_time=True):
                    response = requests.post(
                        "http://mathexpr-ocr-app:8000/ocr",
                        json={"image_base64": base64_image}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        latex_data = result.get("latex")
                        
                        if latex_data and "latex_expression" in latex_data:
                            # Store the original LaTeX expression
                            original_latex = latex_data["latex_expression"]
                            
                            st.success("Image processed successfully!")
                            
                            # Display the extracted LaTeX expression with option to edit
                            st.subheader("Extracted Math Expression:")
                            st.info("You can edit the expression below if the recognition isn't perfect")
                            
                            # Create an editable text area with the recognized expression
                            edited_latex = st.text_area(
                                "Edit LaTeX expression if needed:",
                                value=original_latex,
                                height=150,
                                key="latex_editor"
                            )
                            
                            # Update the LaTeX data with the edited expression
                            latex_data["latex_expression"] = edited_latex
                            st.session_state.latex_data = latex_data
                            st.session_state.current_tab = "verify"
                            
                            # Save the modified LaTeX expression if it differs from the original
                            if edited_latex != original_latex:
                                modified_data = {
                                    "id": latex_data["id"],
                                    "modified_latex": edited_latex
                                }
                                
                                # Save to JSON file
                                modified_file_path = MODIFIED_DIR / f"{latex_data['id']}_modified.json"
                                with open(modified_file_path, "w", encoding="utf-8") as f:
                                    json.dump(modified_data, f, ensure_ascii=False, indent=4)
                                
                                st.info(f"Modified expression saved to {modified_file_path}")
                            
                            # Create a verification button to go to the next tab
                            if st.button("Proceed to Verification"):
                                st.switch_page("verify")
                        else:
                            st.error("No math expression found in the image")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                    
        
        
        else:
            status_placeholder.error("No Image uploaded")

with tab2:
    st.header("Step 2: Validate your solution")

    container = st.container()
    with container:
        status_placeholder = st.empty()

    
