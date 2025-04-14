import streamlit as st

def show():
    """Show the home page"""
    st.title("Welcome to Write2Solve")
    
    # Hero section
    st.markdown("""
    ### Solve handwritten math equations with AI
    
    Upload your handwritten math equations, verify the OCR results, 
    and get step-by-step solutions.
    """)
    
    # Features
    st.subheader("Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### ✏️ OCR for Math")
        st.markdown("Convert handwritten equations to LaTeX with our advanced OCR system")
    
    with col2:
        st.markdown("#### 🔍 Edit & Verify")
        st.markdown("Verify and correct the detected equations before solving")
    
    with col3:
        st.markdown("#### 🧮 Step-by-Step Solutions")
        st.markdown("Get detailed solutions for your math problems")
    
    # How to use
    st.subheader("How to Use")
    st.markdown("""
    1. **Upload** your handwritten equation image
    2. **Verify** the detected equation
    3. **Edit** if necessary
    4. **Solve** to get the step-by-step solution
    5. **Save** to your history for future reference
    """)
    
    # Call to action
    st.markdown("---")
    st.markdown("### Get Started")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Upload Your Equation", use_container_width=True):
            st.session_state.page = "upload_edit"
            st.rerun() 