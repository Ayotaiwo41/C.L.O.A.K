import streamlit as st





#st.write -    this is going to be the home page for the web site we can include quotes and pictures and things of that nature.




st.set_page_config(
    page_title="C.L.O.A.K.fit",
    page_icon="👔",
    layout="wide"
)

if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = []

if 'selected_styles' not in st.session_state:
    st.session_state.selected_styles = []

if 'favorites' not in st.session_state:
    st.session_state.favorites = []

st.title("C.L.O.A.K.fit")
st.subheader("Your AI-Powered Personal Stylist")

st.write("")
st.write("")

st.write("Transform your closet into endless outfit possibilities with AI")

st.write("")
st.write("")
st.write("")

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Get Started", use_container_width=True, type="primary"):
        st.switch_page("1_Your_Closet.py")
