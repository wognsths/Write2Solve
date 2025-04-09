import streamlit as st
import streamlit.components.v1 as components
import os
import base64

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

    if submit_button:
        with container:
            #TODO
            pass