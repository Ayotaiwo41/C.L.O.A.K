import streamlit as st
from utils import go_to_page

def landing_page():
    st.markdown("<h1 class='main-title'>C.L.O.A.K</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>AI-powered outfit recommendations from your closet</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started", key="get_started"):
            go_to_page('closet')
