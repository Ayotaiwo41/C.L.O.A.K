import streamlit as st

st.set_page_config(
    page_title="Your Closet - C.L.O.A.K.fit",
    page_icon="👔",
    layout="wide"
)

st.title("Your Closet")
st.write("Upload images of your clothes")

st.write("")

uploaded_files = st.file_uploader(
    "Choose images", 
    type=['png', 'jpg', 'jpeg'],
    accept_multiple_files=True
)

if uploaded_files:
    st.session_state.uploaded_images = uploaded_files
    
    st.write("")
    st.subheader("Your Items:")
    
    cols = st.columns(4)
    for idx, image in enumerate(uploaded_files):
        with cols[idx % 4]:
            st.image(image, use_column_width=True)

st.write("")
st.write("")

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("← Back", use_container_width=True):
        st.switch_page("home.py")
with col3:
    if st.button("Next →", use_container_width=True, type="primary", disabled=len(st.session_state.uploaded_images)==0):
        st.switch_page("2_Your_Outfits.py")
