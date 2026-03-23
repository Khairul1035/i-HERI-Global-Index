import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# --- 1. GLOBAL SETTINGS ---
st.set_page_config(page_title="i-HERI | Global Health Equity", layout="wide")
PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- 2. SIMULATED REAL-TIME DATA (MARKET INFLATION) ---
# Data ubat global yang naik harga setiap saat
med_market_data = {
    "Treatment": ["Dialysis Kit", "Insulin Pro", "Oncology Phase 1", "Cardiac Stent", "Vaccine Cold-Chain"],
    "Market_Price_2024": [200, 150, 5000, 3500, 80],
    "Current_Market_Price": [245, 185, 6200, 4100, 110], # Real-time simulation
}
df_inflation = pd.DataFrame(med_market_data)
df_inflation['Inflation_Rate'] = ((df_inflation['Current_Market_Price'] - df_inflation['Market_Price_2024']) / df_inflation['Market_Price_2024']) * 100

# --- 3. SIDEBAR ---
st.sidebar.title("🏥 i-HERI INDEX")
st.sidebar.markdown(f"**Principal Investigator:**\n{PI_NAME}")
st.sidebar.divider()
nav = st.sidebar.radio("Global Modules", ["📈 Medical Inflation Tracker", "🛡️ Ethical Hedge Simulator", "🌍 Impact Map (SROI)"])

# --- 4. MODULE 1: INFLATION TRACKER ---
if nav == "📈 Medical Inflation Tracker":
    st.header("📈 Real-Time Medical Inflation Tracker")
    st.write("Tracking global pharmaceutical price hikes and their impact on patient accessibility.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = px.bar(df_inflation, x="Treatment", y="Inflation_Rate", title="Current Global Inflation Rate per Category (%)",
                     color="Inflation_Rate", color_continuous_scale="Reds")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("Avg Global Medical Inflation", "14.2%", "+3.1% YOY")
        st.error("⚠️ ALERT: Dialysis and Oncology costs have exceeded the 'Affordability Threshold' for 65% of the global population.")

# --- 5. MODULE 2: ETHICAL HEDGE SIMULATOR ---
elif nav == "🛡️ Ethical Hedge Simulator":
    st.header("🛡️ Social Capital Hedge (Zakat/Waqf Buffer)")
    st.write("Simulating how Social Impact Capital can neutralize inflation to keep patient bills static.")

    selected_med = st.selectbox("Select Critical Treatment to Hedge", df_inflation['Treatment'])
    row = df_inflation[df_inflation['Treatment'] == selected_med].iloc[0]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Market Price", f"RM {row['Current_Market_Price']}")
    c2.metric("Ethical Target Price", f"RM {row['Market_Price_2024']}")
    
    # Gap to be filled by Zakat/Waqf
    gap = row['Current_Market_Price'] - row['Market_Price_2024']
    c3.metric("Required Social Hedge", f"RM {gap}", delta="Fund Needed", delta_color="inverse")

    st.divider()
    st.subheader("🤖 AI Ethical Auditor (Maqasid Scorecard)")
    social_fund = st.slider("Inject Social Capital (Waqf/Grant) - RM", 0, 5000, int(gap))
    
    resilience_score = (social_fund / gap * 100) if gap > 0 else 100
    
    if resilience_score >= 100:
        st.success(f"✅ RESILIENCE REACHED: Patient bill remains at RM {row['Market_Price_2024']}. Inflation neutralized.")
    else:
        st.warning(f"⚠️ RESILIENCE GAP: Patient still needs to pay RM {row['Current_Market_Price'] - social_fund} extra due to inflation.")

# --- 6. MODULE 3: IMPACT MAP (SROI) ---
elif nav == "🌍 Impact Map (SROI)":
    st.header("🌍 Global Social Return on Investment (SROI)")
    st.write("Visualizing real-time impact of ethical funding on human lives.")
    
    # Dummy data for map
    map_data = pd.DataFrame({
        'lat': [3.1390, -6.2088, 24.7136, 25.2048],
        'lon': [101.6869, 106.8456, 46.6753, 55.2708],
        'Lives_Saved': [1200, 850, 2100, 1400],
        'City': ['Kuala Lumpur', 'Jakarta', 'Riyadh', 'Dubai']
    })
    
    st.map(map_data)
    st.write("### Real-Time Impact Feed")
    st.table(map_data[['City', 'Lives_Saved']])

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center;'><b>i-HERI Project</b> | Principal Investigator: {PI_NAME}</div>", unsafe_allow_html=True)
st.caption("Conceptualized from: Fadzil & Mat (2025). Shariah-Driven Healthcare. RABBANICA, 6(1).")
