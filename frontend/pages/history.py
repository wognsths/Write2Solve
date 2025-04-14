import streamlit as st
import pandas as pd
from datetime import datetime

def show():
    """Show the history page"""
    st.title("Your Equation History")
    
    # Create sample history data
    if "history_data" not in st.session_state:
        st.session_state.history_data = [
            {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "equation": "x^2 + 2x + 1 = 0",
                "solution": "x = -1"
            },
            {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "equation": "\\frac{d}{dx}(x^3 + 2x^2 - 4x + 7)",
                "solution": "3x^2 + 4x - 4"
            }
        ]
    
    # Convert to DataFrame for display
    if st.session_state.history_data:
        df = pd.DataFrame(st.session_state.history_data)
        
        # Display each history item as a card
        for i, row in df.iterrows():
            with st.expander(f"Equation: {row['equation']}", expanded=False):
                st.markdown(f"**Date:** {row['date']}")
                st.markdown(f"**Equation:** ${row['equation']}$")
                st.markdown(f"**Solution:** ${row['solution']}$")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Load to Editor", key=f"load_{i}"):
                        st.session_state.equation_latex = row['equation']
                        st.session_state.page = "upload_edit"
                        st.rerun()
                with col2:
                    if st.button("Delete", key=f"delete_{i}"):
                        st.session_state.history_data.pop(i)
                        st.rerun()
    else:
        st.info("You haven't solved any equations yet. Go to 'Upload & Edit' to get started.")
        
        if st.button("Go to Upload & Edit"):
            st.session_state.page = "upload_edit"
            st.rerun() 