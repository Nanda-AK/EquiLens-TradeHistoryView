import streamlit as st
import pandas as pd
from summary_utils import parse_tradebook

st.set_page_config(page_title="Trade History Visualization", layout="wide")

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='text-align: left; margin-bottom: 10px;'>Trade History Visualization</h1>", unsafe_allow_html=True)

# --- FILE UPLOADER in top-right ---
with st.container():
    col1, col2, col3 = st.columns([4, 1, 2])
    with col3:
        st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

        # ✅ Move success message *inside* the same column
        if uploaded_file:
            try:
                summary_df = parse_tradebook(uploaded_file)
                st.success("✅ Tradebook file upload successfully.")
            except Exception as e:
                st.error(f"❌ Error Tradebook file upload failed: {e}")
                summary_df = None
        else:
            summary_df = None


# --- PROCESS CSV ---
if uploaded_file:
    try:
        summary_df = parse_tradebook(uploaded_file)
        st.success("✅ Tradebook parsed successfully.")

        # Center the summary table
        st.markdown("<div class='table-container'>", unsafe_allow_html=True)
        st.dataframe(summary_df, use_container_width=False)
        st.markdown("</div>", unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
