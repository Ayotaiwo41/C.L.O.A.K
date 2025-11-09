import streamlit as st
from utils import STYLES, go_to_page

def outfits_page():
    st.markdown("# Your Outfits")
    
    if st.session_state.selected_styles:
        st.markdown("### Selected Styles:")
        selected_names = [s['name'] for s in STYLES if s['id'] in st.session_state.selected_styles]
        st.write(", ".join(selected_names))
    
    st.markdown("---")
    
    if not st.session_state.uploaded_images:
        st.warning("Upload clothing items to see outfit recommendations")
        if st.button("Upload Items"):
            go_to_page('closet')
        return
    
    items_per_outfit = min(3, len(st.session_state.uploaded_images))
    num_outfits = 6
    
    cols = st.columns(3)
    for outfit_id in range(num_outfits):
        with cols[outfit_id % 3]:
            st.markdown(f"### Outfit {outfit_id + 1}")
            
            for j in range(items_per_outfit):
                image_index = (outfit_id * items_per_outfit + j) % len(st.session_state.uploaded_images)
                st.image(
                    st.session_state.uploaded_images[image_index]['image'],
                    use_container_width=True
                )
            
            is_liked = outfit_id in st.session_state.liked_outfits
            if st.button(
                "❤️ Liked" if is_liked else "🤍 Like",
                key=f"like_outfit_{outfit_id}"
            ):
                if is_liked:
                    st.session_state.liked_outfits.remove(outfit_id)
                else:
                    st.session_state.liked_outfits.append(outfit_id)
                st.rerun()
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Browse Inspiration", key="browse_inspiration"):
            go_to_page('inspiration')
