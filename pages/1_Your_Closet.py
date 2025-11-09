import streamlit as st
from PIL import Image
import io
st.title("🧥 Your Closet")
st.write("Upload your clothing items below. They’ll be saved in your session for recommendations.")
if "closet_items" not in st.session_state:
    st.session_state.closet_items = []
def image_to_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
uploaded = st.file_uploader("Upload clothing image", type=["png", "jpg", "jpeg"])
if uploaded:
    img = Image.open(uploaded).convert("RGBA")
    st.image(img, caption="Uploaded item preview", use_column_width=True)
    st.session_state.closet_items.append((image_to_bytes(img), uploaded.name))
    st.success("Added to your session closet!")
if st.session_state.closet_items:
    st.write("**Your Closet Items:**")
    cols = st.columns(4)
    for i, (b, name) in enumerate(st.session_state.closet_items):
        cols[i % 4].image(b, width=150, caption=name)
st.markdown("---")
st.page_link("Home.py", label="🏠 Back to Home")
st.page_link("pages/2_Outfit_Recommendations.py", label="➡️ Get Recommendations")
