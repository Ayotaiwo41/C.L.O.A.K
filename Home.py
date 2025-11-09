import streamlit as st

st.set_page_config(page_title="c.l.o.a.k.fit — Outfit Maker", layout="centered")

st.title("👗 c.l.o.a.k.fit — Outfit Maker")
st.write("""
Welcome to **Outfit Maker** — upload clothes to your closet, choose a style, 
and get outfit suggestions powered by AI.
""")

st.markdown("---")
st.subheader("Getting Started")
st.write("Click below to begin building your closet.")

st.page_link("pages/1_Your_Closet.py", label="🚀 Get Started", icon="✨")
