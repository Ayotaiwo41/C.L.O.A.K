import streamlit as st

STYLES = [
    {"id": "y2k", "name": "Y2K"},
    {"id": "streetwear", "name": "Streetwear"},
    {"id": "old-money", "name": "Old Money"},
    {"id": "minimalist", "name": "Minimalist"},
    {"id": "preppy", "name": "Preppy"},
    {"id": "vintage", "name": "Vintage"}
]

def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()
