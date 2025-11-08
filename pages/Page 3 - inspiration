import streamlit as st

st.title("🎨 Style Gallery")

if "selected_style" not in st.session_state:
    st.warning("Please choose a style first in the Outfit Recommendations page.")
    st.page_link("pages/2_Outfit_Recommendations.py", label="⬅️ Go Back")
    st.stop()

style = st.session_state.selected_style
st.subheader(f"Showing inspiration for: {style}")

STYLE_IMAGES = {
    "Y2K": [
        "https://source.unsplash.com/featured/?y2k,fashion",
        "https://source.unsplash.com/featured/?retro,denim"
    ],
    "Streetwear": [
        "https://source.unsplash.com/featured/?streetwear,fashion",
        "https://source.unsplash.com/featured/?urban,style"
    ],
    "Old Money": [
        "https://source.unsplash.com/featured/?preppy,fashion",
        "https://source.unsplash.com/featured/?classic,outfit"
    ]
}

urls = STYLE_IMAGES.get(style, [])
cols = st.columns(2)
for i, url in enumerate(urls):
    with cols[i % 2]:
        st.image(url, caption=f"{style} example {i+1}", use_column_width=True)
        if st.button("💖 Save", key=f"save_{i}"):
            if "favorites" not in st.session_state:
                st.session_state.favorites = []
            st.session_state.favorites.append({"image": url, "desc": f"{style} example {i+1}"})
            st.success("Saved to Favorites!")

st.markdown("---")
st.page_link("pages/2_Outfit_Recommendations.py", label="⬅️ Back to Recommendations")
st.page_link("pages/4_Favorites.py", label="➡️ View Favorites")
