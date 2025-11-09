import streamlit as st
from PIL import Image
import io
import base64

st.title("🧥 Your Closet")
st.write("Upload your clothing items below. Our AI will analyze them to create better outfit recommendations.")

if "closet_items" not in st.session_state:
    st.session_state.closet_items = []

def image_to_bytes(img):
    """Convert PIL image to bytes"""
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def analyze_clothing_with_ai(image_bytes):
    """Use Claude API to analyze the clothing item"""
    try:
        # Convert to base64 for API
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # Call Claude API
        response = fetch("https://api.anthropic.com/v1/messages", {
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
            },
            "body": JSON.stringify({
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": base64_image
                                }
                            },
                            {
                                "type": "text",
                                "text": """Analyze this clothing item and respond ONLY with a JSON object (no markdown, no preamble) with these fields:
{
  "type": "shirt/pants/dress/jacket/shoes/accessory/etc",
  "color": "primary color name",
  "style": "casual/formal/streetwear/vintage/etc",
  "description": "brief 1-sentence description"
}"""
                            }
                        ]
                    }
                ]
            })
        })
        
        data = response.json()
        
        # Extract text from response
        text_content = ""
        for block in data.get("content", []):
            if block.get("type") == "text":
                text_content += block.get("text", "")
        
        # Parse JSON from response
        import json
        analysis = json.loads(text_content.strip())
        return analysis
        
    except Exception as e:
        st.error(f"AI analysis failed: {str(e)}")
        return {
            "type": "unknown",
            "color": "unknown",
            "style": "unknown",
            "description": "Could not analyze"
        }

# File uploader
uploaded = st.file_uploader(
    "Upload clothing image", 
    type=["png", "jpg", "jpeg"],
    help="Upload a clear photo of a single clothing item"
)

if uploaded:
    # Load and display image
    img = Image.open(uploaded).convert("RGBA")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(img, caption="Uploaded item preview", use_column_width=True)
    
    with col2:
        with st.spinner("🤖 AI is analyzing your item..."):
            # Convert to bytes
            img_bytes = image_to_bytes(img)
            
            # Analyze with AI
            analysis = analyze_clothing_with_ai(img_bytes)
            
            # Display analysis
            st.success("✨ AI Analysis Complete!")
            st.write(f"**Type:** {analysis.get('type', 'unknown').title()}")
            st.write(f"**Color:** {analysis.get('color', 'unknown').title()}")
            st.write(f"**Style:** {analysis.get('style', 'unknown').title()}")
            st.write(f"**Description:** {analysis.get('description', 'N/A')}")
    
    # Add to closet button
    if st.button("➕ Add to Closet", type="primary", use_container_width=True):
        # Store image bytes, filename, and AI analysis
        st.session_state.closet_items.append({
            "image_bytes": img_bytes,
            "filename": uploaded.name,
            "analysis": analysis
        })
        st.success("Added to your closet!")
        st.rerun()

# Display closet items
if st.session_state.closet_items:
    st.markdown("---")
    st.subheader(f"👗 Your Closet ({len(st.session_state.closet_items)} items)")
    
    cols = st.columns(4)
    for i, item in enumerate(st.session_state.closet_items):
        with cols[i % 4]:
            st.image(item["image_bytes"], use_column_width=True)
            st.caption(f"**{item['analysis'].get('type', 'Item').title()}**")
            st.caption(f"{item['analysis'].get('color', '')} • {item['analysis'].get('style', '')}")
            
            # Delete button
            if st.button("🗑️", key=f"delete_{i}", help="Remove item"):
                st.session_state.closet_items.pop(i)
                st.rerun()
else:
    st.info("Your closet is empty. Upload your first item to get started!")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.page_link("home.py", label="🏠 Back to Home")
with col2:
    if st.session_state.closet_items:
        st.page_link("pages/2_Outfit_Recommendations.py", label="➡️ Get Recommendations")
    else:
        st.button("➡️ Get Recommendations", disabled=True, help="Add items to your closet first")
