import streamlit as st

st.title("💾 Favorites")

if "favorites" not in st.session_state or not st.session_state.favorites:
    st.info("No favorites saved yet.")
    st.page_link("pages/3_Style_Gallery.py", label="⬅️ Back to Gallery")
    st.stop()

for i, fav in enumerate(st.session_state.favorites):
    st.image(fav["image"], width=300, caption=fav.get("desc", f"Favorite {i+1}"))
    if st.button("🗑 Remove", key=f"remove_{i}"):
        st.session_state.favorites.pop(i)
        st.experimental_rerun()

st.markdown("---")
st.page_link("pages/3_Style_Gallery.py", label="⬅️ Back to Gallery")
st.page_link("Home.py", label="🏠 Back to Home")
