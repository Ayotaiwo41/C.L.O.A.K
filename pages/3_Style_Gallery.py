import streamlit as st
import requests
import json

st.title("🎨 AI Style Gallery & Inspiration")

if "selected_style" not in st.session_state:
    st.warning("Please choose a style first in the Outfit Recommendations page.")
    st.page_link("pages/2_Outfit_Recommendations.py", label="⬅️ Go Back")
    st.stop()

style = st.session_state.selected_style
st.subheader(f"Inspiration for: {style}")

def get_ai_style_guide(style, closet_items):
    """Get AI-generated style guide and tips"""
    try:
        # Prepare closet summary
        closet_summary = []
        for item in closet_items:
            analysis = item.get('analysis', {})
            closet_summary.append({
                "type": analysis.get('type', 'unknown'),
                "color": analysis.get('color', 'unknown'),
                "style": analysis.get('style', 'unknown')
            })
        
        prompt = f"""You are a fashion expert specializing in {style} style. 

The user has these items in their closet:
{json.dumps(closet_summary, indent=2)}

Provide a comprehensive {style} style guide. Respond ONLY with a JSON object (no markdown, no preamble):

{{
  "style_overview": "2-3 sentence overview of {style} style",
  "key_elements": ["element1", "element2", "element3", "element4", "element5"],
  "color_palettes": ["palette1", "palette2", "palette3"],
  "must_have_pieces": ["piece1", "piece2", "piece3", "piece4"],
  "styling_dos": ["do1", "do2", "do3"],
  "styling_donts": ["dont1", "dont2", "dont3"],
  "celebrity_inspiration": ["celebrity1", "celebrity2", "celebrity3"],
  "what_to_add": ["Based on their closet, suggest 2-3 items they should add"],
  "seasonal_tips": "How to adapt this style for different seasons"
}}"""

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
        text_content = ""
        for block in data.get("content", []):
            if block.get("type") == "text":
                text_content += block.get("text", "")
        
        # Clean and parse JSON
        text_content = text_content.strip()
        if text_content.startswith("```"):
            text_content = text_content.split("```")[1]
            if text_content.startswith("json"):
                text_content = text_content[4:]
        
        return json.loads(text_content.strip())
        
    except Exception as e:
        st.error(f"Failed to get style guide: {str(e)}")
        return None

def get_personalized_tips(style, closet_items):
    """Get personalized shopping and styling tips"""
    try:
        closet_summary = []
        for item in closet_items:
            analysis = item.get('analysis', {})
            closet_summary.append(f"{analysis.get('color', '')} {analysis.get('type', 'item')}")
        
        prompt = f"""Based on this {style} closet: {', '.join(closet_summary)}

Give personalized advice. Respond ONLY with JSON (no markdown):

{{
  "missing_pieces": ["What key {style} pieces are they missing?"],
  "next_purchase": "What should they buy next and why?",
  "mixing_tip": "How to mix their current items with new {style} pieces"
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

# Get closet items
closet_items = st.session_state.get('closet_items', [])

# Generate style guide button
if st.button("✨ Get AI Style Guide", type="primary", use_container_width=True):
    with st.spinner(f"🤖 AI is creating your personalized {style} style guide..."):
        style_guide = get_ai_style_guide(style, closet_items)
        if style_guide:
            st.session_state.style_guide = style_guide
            st.success("Style guide ready!")

# Display style guide
if "style_guide" in st.session_state and st.session_state.style_guide:
    guide = st.session_state.style_guide
    
    st.markdown("---")
    
    # Style Overview
    st.markdown("### 📖 Style Overview")
    st.write(guide.get("style_overview", ""))
    
    # Two column layout for key info
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Key Elements")
        for element in guide.get("key_elements", []):
            st.write(f"• {element}")
        
        st.markdown("### 🎨 Color Palettes")
        for palette in guide.get("color_palettes", []):
            st.write(f"• {palette}")
    
    with col2:
        st.markdown("### 👕 Must-Have Pieces")
        for piece in guide.get("must_have_pieces", []):
            st.write(f"• {piece}")
        
        st.markdown("### ⭐ Celebrity Inspiration")
        for celeb in guide.get("celebrity_inspiration", []):
            st.write(f"• {celeb}")
    
    # Styling Do's and Don'ts
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Styling Do's")
        for do in guide.get("styling_dos", []):
            st.success(do)
    
    with col2:
        st.markdown("### ❌ Styling Don'ts")
        for dont in guide.get("styling_donts", []):
            st.error(dont)
    
    # Personalized recommendations
    if closet_items:
        st.markdown("---")
        st.markdown("### 🛍️ Personalized for Your Closet")
        st.info("**What to add next:** " + ", ".join(guide.get("what_to_add", [])))
    
    # Seasonal tips
    st.markdown("---")
    st.markdown("### 🌦️ Seasonal Styling")
    st.write(guide.get("seasonal_tips", ""))

# Personalized shopping tips
if closet_items and st.button("🛒 Get Personalized Shopping Tips"):
    with st.spinner("🤖 Analyzing your closet for personalized advice..."):
        tips = get_personalized_tips(style, closet_items)
        if tips:
            st.session_state.personal_tips = tips

if "personal_tips" in st.session_state and st.session_state.personal_tips:
    tips = st.session_state.personal_tips
    
    st.markdown("---")
    st.markdown("### 🎯 Your Personalized Action Plan")
    
    with st.expander("🔍 What's Missing from Your Closet", expanded=True):
        for item in tips.get("missing_pieces", []):
            st.write(f"• {item}")
    
    with st.expander("💳 Your Next Purchase", expanded=True):
        st.write(tips.get("next_purchase", ""))
    
    with st.expander("🎨 Mixing Old & New", expanded=True):
        st.write(tips.get("mixing_tip", ""))

# Inspiration images (using example URLs)
st.markdown("---")
st.markdown("### 📸 Visual Inspiration")

STYLE_IMAGES = {
    "Y2K": [
        "https://source.unsplash.com/400x600/?y2k,fashion",
        "https://source.unsplash.com/400x600/?retro,colorful,outfit",
        "https://source.unsplash.com/400x600/?2000s,style"
    ],
    "Streetwear": [
        "https://source.unsplash.com/400x600/?streetwear,fashion",
        "https://source.unsplash.com/400x600/?urban,style,sneakers",
        "https://source.unsplash.com/400x600/?hoodie,casual"
    ],
    "Old Money": [
        "https://source.unsplash.com/400x600/?preppy,fashion",
        "https://source.unsplash.com/400x600/?classic,elegant,outfit",
        "https://source.unsplash.com/400x600/?blazer,formal"
    ],
    "Casual Chic": [
        "https://source.unsplash.com/400x600/?casual,chic,fashion",
        "https://source.unsplash.com/400x600/?comfortable,style",
        "https://source.unsplash.com/400x600/?minimal,outfit"
    ]
}

urls = STYLE_IMAGES.get(style, [])
cols = st.columns(3)

for i, url in enumerate(urls):
    with cols[i % 3]:
        st.image(url, caption=f"{style} Inspiration {i+1}", use_column_width=True)
        if st.button("💖 Save", key=f"save_img_{i}", use_container_width=True):
            if "favorites" not in st.session_state:
                st.session_state.favorites = []
            st.session_state.favorites.append({
                "type": "inspiration",
                "image": url, 
                "desc": f"{style} inspiration",
                "style": style
            })
            st.success("Saved to Favorites!")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/2_Outfit_Recommendations.py", label="⬅️ Back to Recommendations")
with col2:
    st.page_link("pages/4_Favorites.py", label="➡️ View Favorites")
