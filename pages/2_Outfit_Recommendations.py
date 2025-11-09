import streamlit as st
import random
import base64

st.title("🪞 Outfit Recommendations")

if "closet_items" not in st.session_state or not st.session_state.closet_items:
    st.warning("No closet items found. Go to 'Your Closet' and upload at least one item.")
    st.page_link("pages/1_Your_Closet.py", label="⬅️ Go to Closet")
    st.stop()

st.write("Choose a style, then generate outfit combinations using items from your closet.")

styles = ["Y2K", "Streetwear", "Old Money"]
style = st.radio("Select your style:", styles)
st.session_state.selected_style = style

def make_outfit_combination(closet_items, style, outfit_num):
    """Create an outfit by combining 2-3 items from the closet"""
    accessories = {
        "Y2K": ["sparkly choker", "chunky sneakers", "butterfly clips"],
        "Streetwear": ["high-top sneakers", "layered tee", "snapback cap"],
        "Old Money": ["loafers", "silk scarf", "leather belt"]
    }
    
    # Shuffle and pick 2-3 items for this outfit
    num_items = min(len(closet_items), random.randint(2, 3))
    outfit_items = random.sample(closet_items, num_items)
    
    acc = random.choice(accessories.get(style, ["belt"]))
    
    return {
        "items": outfit_items,  # List of (bytes, filename) tuples
        "desc": f"{style} Outfit #{outfit_num} — paired with {acc}",
        "style": style
    }

if st.button("Generate Outfits", type="primary"):
    # Check if we have enough items
    if len(st.session_state.closet_items) < 2:
        st.warning("Please upload at least 2 items to generate outfit combinations!")
    else:
        # Generate 3 different outfit combinations
        st.session_state.outfit_cards = [
            make_outfit_combination(st.session_state.closet_items, style, i+1) 
            for i in range(3)
        ]
        st.success("✨ Outfits generated!")

if "outfit_cards" in st.session_state and st.session_state.outfit_cards:
    st.write("### 👗 Suggested Outfits")
    
    # Display in columns for better layout
    cols = st.columns(3)
    
    for idx, outfit in enumerate(st.session_state.outfit_cards):
        with cols[idx % 3]:
            st.write(f"**Outfit {idx + 1}**")
            
            # Display all items in the outfit
            for item_bytes, filename in outfit["items"]:
                st.image(item_bytes, use_column_width=True)
            
            st.write(outfit["desc"])
            
            # Use index-based unique key instead of description
            if st.button("💖 Save to Favorites", key=f"save_outfit_{idx}", use_container_width=True):
                if "favorites" not in st.session_state:
                    st.session_state.favorites = []
                
                # Save the entire outfit with all items
                outfit_data = {
                    "items": [
                        "data:image/png;base64," + base64.b64encode(item_bytes).decode()
                        for item_bytes, _ in outfit["items"]
                    ],
                    "desc": outfit["desc"],
                    "style": outfit["style"]
                }
                st.session_state.favorites.append(outfit_data)
                st.success("Added to Favorites!")
            
            st.divider()

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_Your_Closet.py", label="⬅️ Back to Closet")
with col2:
    st.page_link("pages/3_Style_Gallery.py", label="➡️ Go to Style Gallery")
