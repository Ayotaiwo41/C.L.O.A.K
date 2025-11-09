import streamlit as st
from utils import STYLES, go_to_page

def inspiration_page():
    st.markdown("# Inspiration Gallery")
    st.markdown("### Browse outfit inspiration based on your selected styles")
    
    if not st.session_state.selected_styles:
        st.warning("Please select styles first")
        if st.button("Select Styles"):
            go_to_page('styles')
        return
    
    inspiration_items = []
    for style_id in st.session_state.selected_styles:
        style_name = next(s['name'] for s in STYLES if s['id'] == style_id)
        for i in range(3):
            inspiration_items.append({
                'id': f"{style_id}_{i}",
                'style': style_name,
                'title': f"{style_name} Outfit {i+1}"
            })
    
    cols = st.columns(3)
    for idx, item in enumerate(inspiration_items):
        with cols[idx % 3]:
            st.markdown(f"### {item['title']}")
            st.markdown(f"*Style: {item['style']}*")
            
            st.info(f"Inspiration image for {item['style']} style would appear here")
            
            is_favorited = item['id'] in st.session_state.favorite_inspirations
            if st.button(
                "⭐ Favorited" if is_favorited else "☆ Favorite",
                key=f"fav_{item['id']}"
            ):
                if is_favorited:
                    st.session_state.favorite_inspirations.remove(item['id'])
                else:
                    st.session_state.favorite_inspirations.append(item['id'])
                st.rerun()
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("View Favorites", key="view_favorites"):
            go_to_page('favorites')
