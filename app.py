import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
import time

# --- 1. GLOBAL SETTINGS ---
st.set_page_config(page_title="i-HERI V2 | Global Health Equity", layout="wide")
PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- 2. REAL-TIME DATA SIMULATION (FLUCTUATING PRICES) ---
# Simulasi harga ubat yang berubah sedikit setiap kali refresh
np.random.seed(int(time.time()))
market_prices = {
    "Treatment": ["Dialysis Kit", "Insulin Pro", "Oncology Phase 1", "Cardiac Stent", "Vaccine Cold-Chain"],
    "Base_USD": [50, 40, 1500, 800, 20],
    "Trend": np.random.choice(["▲", "▼", "▬"], 5)
}
df_market = pd.DataFrame(market_prices)

# Exchange Rates (Live Simulation)
rates = {"Malaysia (MYR)": 4.75, "Saudi Arabia (SAR)": 3.75, "USA (USD)": 1.0}

# --- 3. SIDEBAR: THE COMMAND CENTER ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=80)
    st.title("i-HERI INDEX V2")
    st.write(f"**PI:** {PI_NAME}")
    st.divider()
    
    # Real-time Clock
    st.write(f"🕒 **Live Server Time:**\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.divider()
    
    country = st.selectbox("Select Country Benchmark", list(rates.keys()))
    st.divider()
    st.caption("© 2025 i-HERI | Research Reference: Fadzil & Mat (2025)")

# --- 4. DATA PROCESSING ---
rate = rates[country]
df_market['Local_Price'] = df_market['Base_USD'] * rate * (1 + np.random.uniform(-0.05, 0.05, 5))
df_market['Last_Year_Price'] = df_market['Base_USD'] * rate * 0.85 # 15% cheaper last year

# --- 5. MODULES ---
tab1, tab2, tab3 = st.tabs(["📈 Market Inflation Tracker", "🛡️ Social Capital Hedge", "🧠 Research Insights (Loopholes)"])

# --- TAB 1: MARKET TRACKER ---
with tab1:
    st.header(f"📈 {country} Medical Inflation Tracker")
    st.write(f"Tracking live price fluctuations in {country} currency ({rate} multiplier).")
    
    cols = st.columns(len(df_market))
    for i, row in df_market.iterrows():
        color = "normal"
        if row['Trend'] == "▲": color = "inverse"
        cols[i].metric(row['Treatment'], f"{rate:.2f} {row['Local_Price']:,.2f}", f"{row['Trend']} Volatile", delta_color=color)

    st.divider()
    fig = px.bar(df_market, x="Treatment", y=["Last_Year_Price", "Local_Price"], 
                 barmode='group', title=f"Price Comparison: 2024 vs Today ({country})",
                 labels={"value": "Local Currency", "variable": "Year"})
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: HEDGE SIMULATOR ---
with tab2:
    st.header("🛡️ The Ethical Hedge Simulator")
    st.write("Neutralizing inflation through Government & Corporate Cash Injection.")
    
    col_in, col_res = st.columns([1, 1.5])
    
    with col_in:
        st.subheader("📥 Cash Injection Portal")
        gov_cash = st.number_input("Government Grant Injection (RM/SAR)", min_value=0.0, value=50000.0)
        mnc_cash = st.number_input("MNC/Corporate Cash Injection (RM/SAR)", min_value=0.0, value=30000.0)
        zakat_waqf = st.number_input("Social Capital (Zakat/Waqf) (RM/SAR)", min_value=0.0, value=20000.0)
        
        total_buffer = gov_cash + mnc_cash + zakat_waqf
        st.success(f"**Total Hedge Fund:** {rate:.2f} {total_buffer:,.2f}")

    with col_res:
        st.subheader("🧾 Patient Affordability Simulator")
        selected_med = st.selectbox("Select Treatment for Patient", df_market['Treatment'])
        med_price = df_market[df_market['Treatment'] == selected_med]['Local_Price'].values[0]
        
        st.write(f"Actual Market Price: **{rate:.2f} {med_price:,.2f}**")
        
        # Simulation: How much can we cover?
        subsidy_rate = st.slider("Subsidy Coverage per Patient (%)", 0, 100, 50)
        subsidy_val = med_price * (subsidy_rate / 100)
        patient_pays = med_price - subsidy_val
        
        st.markdown(f"""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border-left: 5px solid #1E3A8A;">
            <h3>Final Patient Bill: {rate:.2f} {patient_pays:,.2f}</h3>
            <p>Hedge Buffer Applied: - {rate:.2f} {subsidy_val:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sustainability Check
        capacity = total_buffer / subsidy_val if subsidy_val > 0 else 0
        st.info(f"💡 Based on your Injection, this fund can support **{int(capacity)} patients** for {selected_med} before depletion.")

# --- TAB 3: LOOPHOLES & INSIGHTS ---
with tab3:
    st.header("🧠 7 Hidden Loopholes Burdening Patients")
    st.write("Addressing the systemic failures that Government & Companies must resolve.")
    
    loopholes = {
        "1. Currency Volatility": "Most drugs are USD-based. Local patients suffer when the currency drops. **Gov Solution:** Sovereign Med-Reserves.",
        "2. Middleman Markups": "Supply chains add 30-50% margin. **Company Solution:** Direct Factory-to-Hospital Procurement.",
        "3. Patent Monopolies": "Branded drugs are too expensive. **Gov Solution:** Incentivize High-Quality Generics.",
        "4. Logistics Failure": "Loss of cold-chain meds (vials) increases costs. **Company Solution:** IoT-tracked cold storage.",
        "5. Diagnostic Over-testing": "Defensive medicine costs patients millions. **Gov Solution:** Clear Clinical Malpractice Guidelines.",
        "6. Preventive Care Gap": "Insurance covers surgery, but not nutrition/prevention. **Gov Solution:** Tax-rebates for preventive care.",
        "7. Re-hospitalization Risk": "Poor home-care leads to relapse. **Social Solution:** Waqf-funded Home-Care Support Teams."
    }
    
    for l, d in loopholes.items():
        with st.expander(l):
            st.write(d)

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center;'><b>i-HERI Global Sustainability Project</b> | Principal Investigator: {PI_NAME}</div>", unsafe_allow_html=True)
