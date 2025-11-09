import streamlit as st
import random
import base64

st.title("🪞 Outfit Recommendations")

if "closet_items" not in st.session_state or not st.session_state.closet_items:
    st.warning("No closet items found. Go to 'Your Closet' and upload at least one item.")
    st.page_link("pages/1_Your_Closet.py", label="⬅️ Go to Closet")
    st.stop()

st.write("Choose a style, then generate simple outfit combinations.")

styles = ["Y2K", "Streetwear", "Old Money"]
style = st.radio("Select your style:", styles)
st.session_state.selected_style = style

def make_mock_outfit(item_bytes, style):
    accessories = {
        "Y2K": ["sparkly choker", "chunky sneakers"],
        "Streetwear": ["high-top sneakers", "layered tee"],
        "Old Money": ["loafers", "silk scarf"]
    }
    acc = random.choice(accessories.get(style, ["belt"]))
    return {
        "item": item_bytes,
        "desc": f"{style} look — paired with {acc}."
    }

if st.button("Generate Outfits"):
    st.session_state.outfit_cards = [
        make_mock_outfit(b, style) for b, _ in st.session_state.closet_items
    ]

if "outfit_cards" in st.session_state:
    st.write("### Suggested Outfits")
    for outfit in st.session_state.outfit_cards:
        st.image(outfit["item"], width=200)
        st.write(outfit["desc"])
        if st.button("💖 Save to Favorites", key=outfit["desc"]):
            if "favorites" not in st.session_state:
                st.session_state.favorites = []
            data_uri = "data:image/png;base64," + base64.b64encode(outfit["item"]).decode()
            st.session_state.favorites.append({"image": data_uri, "desc": outfit["desc"]})
            st.success("Added to Favorites!")

st.markdown("---")
st.page_link("pages/1_Your_Closet.py", label="⬅️ Back to Closet")
st.page_link("pages/3_Style_Gallery.py", label="➡️ Go to Style Gallery")
