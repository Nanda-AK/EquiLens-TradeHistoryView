import streamlit as st
import pandas as pd
from summary_utils import parse_tradebook

st.set_page_config(page_title="Trade Summary | Zerodha", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS styling
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📈 Trade Summary (Zerodha Tradebook)")
st.markdown("Upload your Zerodha tradebook CSV file below to view a summarized breakdown.")

uploaded_file = st.file_uploader("Upload Zerodha Tradebook CSV", type=["csv"])

if uploaded_file:
    try:
        summary_df = parse_tradebook(uploaded_file)
        st.success("✅ Tradebook parsed successfully.")
        st.dataframe(summary_df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
