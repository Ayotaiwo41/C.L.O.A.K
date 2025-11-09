import streamlit as st
from utils import STYLES, go_to_page

def style_selection_page():
    st.markdown("# Choose Your Style")
    st.markdown("### Select one or more styles to personalize your outfit recommendations")
    
    cols = st.columns(3)
    for idx, style in enumerate(STYLES):
        with cols[idx % 3]:
            is_selected = style['id'] in st.session_state.selected_styles
            
            with st.container():
                st.markdown(f"### {style['name']}")
                
                if st.button(
                    "✓ Selected" if is_selected else "Select",
                    key=f"style_{style['id']}",
                    type="primary" if is_selected else "secondary"
                ):
                    if is_selected:
                        st.session_state.selected_styles.remove(style['id'])
                    else:
                        st.session_state.selected_styles.append(style['id'])
                    st.rerun()
    
    if st.session_state.selected_styles:
        st.markdown("---")
        st.markdown("### Selected Styles:")
        selected_names = [s['name'] for s in STYLES if s['id'] in st.session_state.selected_styles]
        st.write(", ".join(selected_names))
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Generate Outfits", key="generate_outfits"):
                go_to_page('outfits')
