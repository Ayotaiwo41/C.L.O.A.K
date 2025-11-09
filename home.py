import streamlit as st

st.set_page_config(page_title="c.l.o.a.k.fit — AI Outfit Maker", layout="centered")

# Initialize all session state variables
if 'closet_items' not in st.session_state:
    st.session_state.closet_items = []

if 'selected_style' not in st.session_state:
    st.session_state.selected_style = None

if 'favorites' not in st.session_state:
    st.session_state.favorites = []

if 'outfit_cards' not in st.session_state:
    st.session_state.outfit_cards = []

# Header
st.title("👔 C.L.O.A.K")
st.subheader("AI-Powered Outfit Creator")

st.write("""
Welcome to **C.L.O.A.K** — your personal AI stylist! 

Say goodbye to outfit anxiety and hello to confidence! 

Our AI analyzes your clothing items and creates perfect outfit combinations 
tailored to your chosen style.
""")

# Features
st.markdown("---")
st.subheader("✨ How It Works")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📸 Upload")
    st.write("Add photos of your clothes to build your digital closet")

with col2:
    st.markdown("### 🎨 Style")
    st.write("Choose from Y2K, Streetwear, or Old Money aesthetics")

with col3:
    st.markdown("### 🤖 AI Magic")
    st.write("Get smart outfit combinations powered by AI")

st.markdown("---")

# Display current closet stats
if st.session_state.closet_items:
    st.info(f"👗 You currently have **{len(st.session_state.closet_items)} items** in your closet")

# Get Started Button
st.subheader("Ready to Get Started?")
st.write("Click below to begin building your closet.")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.page_link("pages/1_Your_Closet.py", label="🚀 Start Building Your Closet", icon="✨")

# Footer
st.markdown("---")
st.caption("Powered by Claude AI • Made with ❤️ for fashion lovers")
