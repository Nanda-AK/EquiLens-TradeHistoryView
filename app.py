import streamlit as st
import pandas as pd
from summary_utils import parse_tradebook
from summary_utils import get_trade_date_range

st.set_page_config(page_title="Trade History Visualization", layout="wide")

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>Trade History Visualization</h1>", unsafe_allow_html=True)

# --- FILE UPLOADER in top-right ---
with st.container():
    col1, col2, col3 = st.columns([4, 1, 2])
    with col3:
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

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
            df = pd.read_csv(uploaded_file)
            oldest_date, latest_date = get_trade_date_range(uploaded_file)
            summary_df = parse_tradebook(uploaded_file)
            
    
            # Recommended layout: center the table using Streamlit's grid
            left, center, right = st.columns([1, 6, 1])

            with center:

                # Subheader
                #st.subheader("Trade Summary")
                st.subheader(f"Trade Summary between {oldest_date} to {latest_date}")
                
                # Row styling for Buy/Sell
                def highlight_buysell(row):
                    if row['Buy/Sell Type'].upper() == 'BUY':
                        return ['background-color: #144d3f; color: white'] * len(row)
                    elif row['Buy/Sell Type'].upper() == 'SELL':
                        return ['background-color: #4a1f1f; color: white'] * len(row)
                    else:
                        return [''] * len(row)
                
                # Format + style
                styled_df = (
                    summary_df
                    .style
                    .apply(highlight_buysell, axis=1)
                    .format({
                        'Quantity': '{:,.0f}',       # No decimal
                        'Avg_Price': '{:,.2f}',      # Two decimal
                        'Total_Value': '{:,.0f}'     # No decimal
                    })
                )
                
                # Display
                st.dataframe(styled_df, use_container_width=True, height=500)
     


            
        except Exception as e:
            st.error(f"❌ Error processing file: {e}")
