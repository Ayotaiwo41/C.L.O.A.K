import streamlit as st
from pages.landing import landing_page
from pages.closet import closet_page
from pages.styles import style_selection_page
from pages.outfits import outfits_page
from pages.inspiration import inspiration_page
from pages.favorites import favorites_page

st.set_page_config(
    page_title="C.L.O.A.K",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = []
if 'selected_styles' not in st.session_state:
    st.session_state.selected_styles = []
if 'liked_outfits' not in st.session_state:
    st.session_state.liked_outfits = []
if 'favorite_inspirations' not in st.session_state:
    st.session_state.favorite_inspirations = []

st.markdown("""
<style>
    .main-title {
        font-size: 4rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .style-card {
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
    }
    .style-card-selected {
        border: 3px solid #FF4B4B;
        background-color: #FFE6E6;
    }
    .outfit-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #FF3333;
    }
</style>
""", unsafe_allow_html=True)

def main():
    with st.sidebar:
        st.markdown("## Navigation")
        if st.button("🏠 Home", key="nav_home"):
            st.session_state.page = 'landing'
            st.rerun()
        if st.button("👕 Your Closet", key="nav_closet"):
            st.session_state.page = 'closet'
            st.rerun()
        if st.button("🎨 Styles", key="nav_styles"):
            st.session_state.page = 'styles'
            st.rerun()
        if st.button("👔 Outfits", key="nav_outfits"):
            st.session_state.page = 'outfits'
            st.rerun()
        if st.button("🌟 Inspiration", key="nav_inspiration"):
            st.session_state.page = 'inspiration'
            st.rerun()
        if st.button("⭐ Favorites", key="nav_favorites"):
            st.session_state.page = 'favorites'
            st.rerun()
    
    if st.session_state.page == 'landing':
        landing_page()
    elif st.session_state.page == 'closet':
        closet_page()
    elif st.session_state.page == 'styles':
        style_selection_page()
    elif st.session_state.page == 'outfits':
        outfits_page()
    elif st.session_state.page == 'inspiration':
        inspiration_page()
    elif st.session_state.page == 'favorites':
        favorites_page()

if __name__ == "__main__":
    main()
