import streamlit as st
from frontend.pages import home, upload_edit, verify, history

# Set page configuration
st.set_page_config(
    page_title="Write2Solve",
    page_icon="✏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state if not exists
if "page" not in st.session_state:
    st.session_state.page = "home"
if "equation_latex" not in st.session_state:
    st.session_state.equation_latex = ""
if "rendered_latex" not in st.session_state:
    st.session_state.rendered_latex = ""

# Navigation sidebar
st.sidebar.title("Write2Solve")
st.sidebar.image("https://via.placeholder.com/150x80?text=Write2Solve", width=150)

# Navigation
page = st.sidebar.radio(
    "Navigate to",
    ["Home", "Upload & Edit", "Verify Solution", "History"],
    index=0
)

# Page routing
if page == "Home":
    st.session_state.page = "home"
    home.show()
elif page == "Upload & Edit":
    st.session_state.page = "upload_edit"
    upload_edit.show()
elif page == "Verify Solution":
    st.session_state.page = "verify"
    verify.show()
elif page == "History":
    st.session_state.page = "history"
    history.show()

# Footer
st.sidebar.markdown("---")
st.sidebar.info(
    "Write2Solve helps you solve handwritten math equations with AI."
)

if __name__ == "__main__":
    # This is used when running the file directly
    pass
