import streamlit as st
import base64
import requests
import json

st.title("🪞 AI Outfit Recommendations")

if "closet_items" not in st.session_state or not st.session_state.closet_items:
    st.warning("No closet items found. Go to 'Your Closet' and upload at least one item.")
    st.page_link("pages/1_Your_Closet.py", label="⬅️ Go to Closet")
    st.stop()

st.write("Choose a style, and our AI will create perfect outfit combinations from your closet items.")

# Style selection
styles = ["Y2K", "Streetwear", "Old Money", "Casual Chic"]
style = st.radio("Select your style:", styles, horizontal=True)
st.session_state.selected_style = style

# Display closet summary
st.info(f"🧥 Using {len(st.session_state.closet_items)} items from your closet")

def generate_ai_outfits(closet_items, style, num_outfits=3):
    """Use Claude AI to generate smart outfit combinations"""
    try:
        # Prepare clothing inventory for AI
        inventory = []
        for idx, item in enumerate(closet_items):
            analysis = item.get('analysis', {})
            inventory.append({
                "id": idx,
                "type": analysis.get('type', 'unknown'),
                "color": analysis.get('color', 'unknown'),
                "style": analysis.get('style', 'unknown'),
                "description": analysis.get('description', '')
            })
        
        # Create prompt for AI
        prompt = f"""You are a professional fashion stylist. Based on the following clothing items, create {num_outfits} complete {style} outfits.

Available clothing items:
{json.dumps(inventory, indent=2)}

Requirements:
- Each outfit should have 2-4 compatible items
- Consider color coordination, style matching, and the {style} aesthetic
- Provide styling tips for each outfit
- Respond ONLY with a JSON array (no markdown, no preamble) in this format:

[
  {{
    "outfit_number": 1,
    "item_ids": [0, 2, 3],
    "why_it_works": "Brief explanation of why these items work together",
    "styling_tips": "How to wear this outfit",
    "occasion": "Best occasion for this outfit"
  }}
]"""

        # Call Claude API
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": st.secrets["ANTHROPIC_API_KEY"]
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 2000,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }]
            }
        )
        
        data = response.json()
        
        # Extract text content
        text_content = ""
        for block in data.get("content", []):
            if block.get("type") == "text":
                text_content += block.get("text", "")
        
        # Parse JSON response
        text_content = text_content.strip()
        # Remove markdown code blocks if present
        if text_content.startswith("```"):
            text_content = text_content.split("```")[1]
            if text_content.startswith("json"):
                text_content = text_content[4:]
        
        outfits = json.loads(text_content.strip())
        
        # Build outfit objects with actual items
        result = []
        for outfit in outfits:
            outfit_items = [closet_items[i] for i in outfit["item_ids"] if i < len(closet_items)]
            result.append({
                "items": outfit_items,
                "why_it_works": outfit.get("why_it_works", ""),
                "styling_tips": outfit.get("styling_tips", ""),
                "occasion": outfit.get("occasion", ""),
                "style": style
            })
        
        return result
        
    except Exception as e:
        st.error(f"AI outfit generation failed: {str(e)}")
        return []

# Generate outfits button
if st.button("🤖 Generate AI Outfits", type="primary", use_container_width=True):
    # Check if we have enough items
    if len(st.session_state.closet_items) < 2:
        st.warning("Please upload at least 2 items to generate outfit combinations!")
    else:
        with st.spinner("🎨 AI is creating your perfect outfits..."):
            # Generate AI-powered outfits
            st.session_state.outfit_cards = generate_ai_outfits(
                st.session_state.closet_items, 
                style,
                num_outfits=3
            )
            
            if st.session_state.outfit_cards:
                st.success("✨ Your outfits are ready!")
            else:
                st.error("Failed to generate outfits. Please try again.")

# Display generated outfits
if "outfit_cards" in st.session_state and st.session_state.outfit_cards:
    st.markdown("---")
    st.subheader("👗 Your AI-Generated Outfits")
    
    for idx, outfit in enumerate(st.session_state.outfit_cards):
        st.markdown(f"### Outfit {idx + 1}")
        
        # Display outfit items in columns
        cols = st.columns(len(outfit["items"]))
        for i, item in enumerate(outfit["items"]):
            with cols[i]:
                st.image(item["image_bytes"], use_column_width=True)
                analysis = item.get('analysis', {})
                st.caption(f"**{analysis.get('type', 'Item').title()}**")
                st.caption(f"{analysis.get('color', '')} {analysis.get('style', '')}")
        
        # Display AI insights
        with st.expander("💡 AI Styling Insights", expanded=True):
            st.write(f"**Why it works:** {outfit.get('why_it_works', 'N/A')}")
            st.write(f"**Styling tips:** {outfit.get('styling_tips', 'N/A')}")
            st.write(f"**Best for:** {outfit.get('occasion', 'N/A')}")
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💖 Save to Favorites", key=f"save_outfit_{idx}", use_container_width=True):
                if "favorites" not in st.session_state:
                    st.session_state.favorites = []
                
                # Save the entire outfit with all items and AI insights
                outfit_data = {
                    "items": [
                        {
                            "image": "data:image/png;base64," + base64.b64encode(item["image_bytes"]).decode(),
                            "analysis": item.get("analysis", {})
                        }
                        for item in outfit["items"]
                    ],
                    "why_it_works": outfit.get("why_it_works", ""),
                    "styling_tips": outfit.get("styling_tips", ""),
                    "occasion": outfit.get("occasion", ""),
                    "style": outfit["style"]
                }
                st.session_state.favorites.append(outfit_data)
                st.success("Added to Favorites!")
        
        with col2:
            if st.button("🔄 Regenerate This Outfit", key=f"regen_{idx}", use_container_width=True):
                st.info("Regenerating outfits... Click 'Generate AI Outfits' again!")
        
        st.divider()

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_Your_Closet.py", label="⬅️ Back to Closet")
with col2:
    st.page_link("pages/3_Style_Gallery.py", label="➡️ Go to Style Gallery")
