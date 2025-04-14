import streamlit as st
from frontend.components import latex_renderer, solution_display
from frontend.utils import api_client

def show():
    st.title("Verify Solution")
    
    # Check if we have an equation
    if not st.session_state.get("equation_latex"):
        st.warning("No equation to verify. Please upload and process an equation first.")
        
        if st.button("Go to Upload & Edit"):
            st.session_state.page = "upload_edit"
            st.experimental_rerun()
        return
    
    # Display the equation
    st.subheader("Your Equation")
    latex_renderer.display_equation(st.session_state.rendered_latex)
    
    # Solution input
    st.subheader("Enter Your Solution")
    solution = st.text_area(
        "Type your solution here",
        height=150,
        help="Enter your step-by-step solution to the equation"
    )
    
    # Verify button
    if solution and st.button("Verify Solution"):
        with st.spinner("Verifying solution..."):
            # Call verification API
            verification_result = api_client.verify_solution(
                st.session_state.equation_latex,
                solution
            )
            
            if verification_result:
                # Save result to session state
                st.session_state.verification_result = verification_result
                
                # Show result
                st.subheader("Verification Result")
                solution_display.show_verification(verification_result)
            else:
                st.error("Failed to verify solution. Please try again.")
    
    # If we have a verification result, display it
    elif "verification_result" in st.session_state:
        st.subheader("Verification Result")
        solution_display.show_verification(st.session_state.verification_result)
    
    # Back to edit button
    if st.button("Back to Edit Equation"):
        st.session_state.page = "upload_edit"
        st.experimental_rerun()
