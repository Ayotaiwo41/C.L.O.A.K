import streamlit as st
from PIL import Image
import io
from utils import go_to_page

def closet_page():
    st.markdown("# Your Closet")
    st.markdown("### Upload photos of your clothing items")
    
    uploaded_files = st.file_uploader(
        "Drag photos here or click to browse",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        key="file_uploader"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            image_bytes = uploaded_file.read()
            if image_bytes not in [img['bytes'] for img in st.session_state.uploaded_images]:
                image = Image.open(io.BytesIO(image_bytes))
                st.session_state.uploaded_images.append({
                    'bytes': image_bytes,
                    'image': image,
                    'name': uploaded_file.name
                })
    
    if st.session_state.uploaded_images:
        st.markdown("---")
        st.markdown("### Your Items")
        
        cols = st.columns(4)
        for idx, img_data in enumerate(st.session_state.uploaded_images):
            with cols[idx % 4]:
                st.image(img_data['image'], use_container_width=True)
                if st.button("Remove", key=f"remove_{idx}"):
                    st.session_state.uploaded_images.pop(idx)
                    st.rerun()
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Continue to Style Selection", key="continue_to_styles"):
                go_to_page('styles')
