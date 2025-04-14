import streamlit as st
import json

def show():
    """Show the verify solution page"""
    st.title("Verify Solution")
    
    # Check if we have an equation to work with
    if not st.session_state.get("equation_latex"):
        st.warning("No equation to verify. Please upload and process an equation first.")
        
        if st.button("Go to Upload & Edit"):
            st.session_state.page = "upload_edit"
            st.rerun()
        return
        
    # Display current equation
    st.subheader("Your Equation")
    st.latex(st.session_state.equation_latex)
    
    # Solution generation section
    st.subheader("Generate Solution")
    
    # Options for solution
    solution_type = st.radio(
        "Solution Type",
        ["Step-by-Step", "Final Answer Only"],
        index=0
    )
    
    detail_level = st.select_slider(
        "Detail Level",
        options=["Basic", "Intermediate", "Detailed"],
        value="Intermediate"
    )
    
    # Generate solution button
    if st.button("Solve Equation"):
        with st.spinner("Generating solution..."):
            # Simulate API call with a fake response
            solution = {
                "steps": [
                    {"explanation": "Identify the equation type: quadratic equation in standard form $ax^2 + bx + c = 0$", 
                     "latex": "x^2 + 2x + 1 = 0"},
                    {"explanation": "Factor the equation", 
                     "latex": "(x + 1)^2 = 0"},
                    {"explanation": "Solve for x", 
                     "latex": "x = -1"}
                ],
                "final_answer": "x = -1"
            }
            
            # Display solution
            st.success("Solution generated!")
            
            if solution_type == "Step-by-Step":
                st.subheader("Step-by-Step Solution")
                for i, step in enumerate(solution["steps"]):
                    with st.expander(f"Step {i+1}", expanded=True):
                        st.write(step["explanation"])
                        st.latex(step["latex"])
            
            st.subheader("Final Answer")
            st.latex(solution["final_answer"])
            
            # Save to history option
            if st.button("Save to History"):
                if "history_data" not in st.session_state:
                    st.session_state.history_data = []
                    
                # Add current problem to history
                import datetime
                st.session_state.history_data.append({
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "equation": st.session_state.equation_latex,
                    "solution": solution["final_answer"]
                })
                
                st.success("Saved to history!")
                
                # Option to go to history
                if st.button("View History"):
                    st.session_state.page = "history"
                    st.rerun()
