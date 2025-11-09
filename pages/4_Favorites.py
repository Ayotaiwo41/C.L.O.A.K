import streamlit as st
import requests
import json

st.title("💖 Your Favorites")

if "favorites" not in st.session_state or not st.session_state.favorites:
    st.info("No favorites saved yet. Start by generating outfits or browsing the style gallery!")
    col1, col2 = st.columns(2)
    with col1:
        st.page_link("pages/2_Outfit_Recommendations.py", label="📸 Generate Outfits")
    with col2:
        st.page_link("pages/3_Style_Gallery.py", label="🎨 Browse Gallery")
    st.stop()

st.write(f"You have **{len(st.session_state.favorites)}** saved favorites")

def get_outfit_variations(outfit_data):
    """Get AI suggestions for outfit variations"""
    try:
        # Prepare outfit details
        items_desc = []
        for item in outfit_data.get("items", []):
            if isinstance(item, dict):
                analysis = item.get("analysis", {})
                items_desc.append(f"{analysis.get('color', '')} {analysis.get('type', 'item')}")
        
        prompt = f"""This outfit contains: {', '.join(items_desc)}

Style: {outfit_data.get('style', 'casual')}

Provide 3 creative variations of this outfit. Respond ONLY with JSON (no markdown):

{{
  "variations": [
    {{
      "name": "variation name",
      "changes": "what to add/swap/remove",
      "occasion": "best for what occasion",
      "vibe": "how it changes the vibe"
    }}
  ]
}}"""

        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": st.secrets["ANTHROPIC_API_KEY"]
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }]
            }
        )
        
        data = response.json()
        text_content = ""
        for block in data.get("content", []):
            if block.get("type") == "text":
                text_content += block.get("text", "")
        
        text_content = text_content.strip()
        if text_content.startswith("```"):
            text_content = text_content.split("```")[1]
            if text_content.startswith("json"):
                text_content = text_content[4:]
        
        return json.loads(text_content.strip())
        
    except Exception as e:
        return None

def analyze_favorite_collection():
    """Analyze all favorites to identify style patterns"""
    try:
        # Gather all outfit details
        collection_summary = []
        for fav in st.session_state.favorites:
            if fav.get("type") != "inspiration":
                collection_summary.append({
                    "style": fav.get("style", "unknown"),
                    "occasion": fav.get("occasion", ""),
                    "items_count": len(fav.get("items", []))
                })
        
        if not collection_summary:
            return None
        
        prompt = f"""Analyze this collection of saved outfits:
{json.dumps(collection_summary, indent=2)}

Provide insights. Respond ONLY with JSON (no markdown):

{{
  "dominant_style": "what style appears most",
  "style_personality": "describe their fashion personality in 1-2 sentences",
  "versatility_score": "rate 1-10 how versatile their favorites are",
  "recommendations": ["3 specific suggestions to diversify or enhance their collection"],
  "signature_look": "what seems to be their signature/go-to look"
}}"""

        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": st.secrets["ANTHROPIC_API_KEY"]
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }]
            }
        )
        
        data = response.json()
        text_content = ""
        for block in data.get("content", []):
            if block.get("type") == "text":
                text_content += block.get("text", "")
        
        text_content = text_content.strip()
        if text_content.startswith("```"):
            text_content = text_content.split("```")[1]
            if text_content.startswith("json"):
                text_content = text_content[4:]
        
        return json.loads(text_content.strip())
        
    except Exception as e:
        return None

# Analyze collection button
if len(st.session_state.favorites) >= 2:
    if st.button("🔍 Analyze My Style Collection", type="primary", use_container_width=True):
        with st.spinner("🤖 AI is analyzing your fashion preferences..."):
            analysis = analyze_favorite_collection()
            if analysis:
                st.session_state.collection_analysis = analysis

# Display collection analysis
if "collection_analysis" in st.session_state and st.session_state.collection_analysis:
    analysis = st.session_state.collection_analysis
    
    st.markdown("---")
    st.markdown("### 🎭 Your Style Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Dominant Style", analysis.get("dominant_style", "Mixed"))
        st.metric("Versatility Score", f"{analysis.get('versatility_score', 'N/A')}/10")
    
    with col2:
        st.markdown("**Your Fashion Personality:**")
        st.write(analysis.get("style_personality", ""))
    
    st.markdown("**Your Signature Look:**")
    st.info(analysis.get("signature_look", ""))
    
    st.markdown("**Recommendations to Enhance Your Collection:**")
    for rec in analysis.get("recommendations", []):
        st.write(f"• {rec}")
    
    st.markdown("---")

# Display favorites
st.subheader("📁 Saved Outfits & Inspiration")

# Filter options
filter_type = st.radio(
    "Filter by:",
    ["All", "Outfits", "Inspiration"],
    horizontal=True
)

# Filter favorites
filtered_favorites = st.session_state.favorites
if filter_type == "Outfits":
    filtered_favorites = [f for f in st.session_state.favorites if f.get("type") != "inspiration"]
elif filter_type == "Inspiration":
    filtered_favorites = [f for f in st.session_state.favorites if f.get("type") == "inspiration"]

# Display each favorite
for i, fav in enumerate(filtered_favorites):
    st.markdown(f"### Favorite #{i+1}")
    
    # Check if it's an outfit or inspiration image
    if fav.get("type") == "inspiration":
        # Simple inspiration image
        st.image(fav.get("image"), width=400, caption=fav.get("desc", "Inspiration"))
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑️ Remove", key=f"remove_{i}"):
                st.session_state.favorites.pop(i)
                st.rerun()
    
    else:
        # Full outfit with items
        items = fav.get("items", [])
        
        # Display outfit images
        if items:
            cols = st.columns(min(len(items), 4))
            for idx, item in enumerate(items):
                with cols[idx % 4]:
                    if isinstance(item, dict):
                        st.image(item.get("image"), use_column_width=True)
                        analysis = item.get("analysis", {})
                        st.caption(f"{analysis.get('type', 'Item').title()}")
                    else:
                        st.image(item, use_column_width=True)
        
        # Display outfit details
        with st.expander("📝 Outfit Details", expanded=False):
            st.write(f"**Style:** {fav.get('style', 'N/A')}")
            if fav.get('why_it_works'):
                st.write(f"**Why it works:** {fav.get('why_it_works')}")
            if fav.get('styling_tips'):
                st.write(f"**Styling tips:** {fav.get('styling_tips')}")
            if fav.get('occasion'):
                st.write(f"**Best for:** {fav.get('occasion')}")
        
        # Action buttons
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            if st.button("✨ Get Variations", key=f"vary_{i}"):
                with st.spinner("🤖 Creating outfit variations..."):
                    variations = get_outfit_variations(fav)
                    if variations:
                        st.session_state[f"variations_{i}"] = variations
        
        with col2:
            if st.button("📤 Share Outfit", key=f"share_{i}"):
                st.success("Sharing feature coming soon!")
        
        with col3:
            if st.button("🗑️", key=f"remove_{i}", help="Remove from favorites"):
                st.session_state.favorites.pop(i)
                st.rerun()
        
        # Display variations if generated
        if f"variations_{i}" in st.session_state:
            variations_data = st.session_state[f"variations_{i}"]
            st.markdown("**💡 Try These Variations:**")
            
            for var in variations_data.get("variations", []):
                with st.container():
                    st.markdown(f"**{var.get('name')}**")
                    st.write(f"🔄 {var.get('changes')}")
                    st.write(f"📍 {var.get('occasion')}")
                    st.write(f"✨ {var.get('vibe')}")
                    st.divider()
    
    st.markdown("---")

# Export/Clear options
st.markdown("### 🛠️ Manage Favorites")
col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Export Collection", use_container_width=True):
        st.info("Export feature coming soon! You'll be able to download your favorites as a PDF.")

with col2:
    if st.button("🗑️ Clear All Favorites", use_container_width=True):
        if st.session_state.favorites:
            st.warning("Are you sure? This will delete all your favorites.")
            if st.button("⚠️ Yes, Clear Everything"):
                st.session_state.favorites = []
                if "collection_analysis" in st.session_state:
                    del st.session_state.collection_analysis
                st.rerun()

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/3_Style_Gallery.py", label="⬅️ Back to Gallery")
with col2:
    st.page_link("pages/2_Outfit_Recommendations.py", label="🔄 Get More Outfits")
with col3:
    st.page_link("home.py", label="🏠 Back to Home")
