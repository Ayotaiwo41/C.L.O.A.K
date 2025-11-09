import streamlit as st
from utils import STYLES, go_to_page

def favorites_page():
    st.markdown("# Your Favorites")
    st.markdown("### Saved inspiration for outfit ideas")
    
    if not st.session_state.favorite_inspirations:
        st.info("You haven't favorited any inspiration yet")
        if st.button("Browse Inspiration"):
            go_to_page('inspiration')
        return
    
    st.write(f"You have {len(st.session_state.favorite_inspirations)} favorite(s)")
    
    for fav_id in st.session_state.favorite_inspirations:
        parts = fav_id.split('_')
        style_id = parts[0]
        style_name = next(s['name'] for s in STYLES if s['id'] == style_id)
        
        with st.container():
            st.markdown(f"### {style_name} Outfit")
            st.info(f"Favorited inspiration image would appear here")
            if st.button("Remove from Favorites", key=f"remove_fav_{fav_id}"):
                st.session_state.favorite_inspirations.remove(fav_id)
                st.rerun()
            st.markdown("---")
