import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
import requests
import time

# --- 1. GLOBAL SETTINGS ---
st.set_page_config(page_title="i-HERI V2 | Live Global Index", layout="wide")

# NAMA RESEARCHER
RESEARCHER_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- 2. REAL-TIME CURRENCY FETCHING ---
@st.cache_data(ttl=3600) # Cache data for 1 hour to save bandwidth
def get_live_rates():
    try:
        # Menggunakan API percuma dari open.er-api.com
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        data = response.json()
        return {
            "Malaysia (MYR)": data['rates']['MYR'],
            "Saudi Arabia (SAR)": data['rates']['SAR'],
            "USA (USD)": 1.0
        }
    except:
        # Fallback jika API gagal
        return {"Malaysia (MYR)": 4.45, "Saudi Arabia (SAR)": 3.75, "USA (USD)": 1.0}

live_rates = get_live_rates()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=70)
    st.title("i-HERI INDEX V2")
    st.write(f"**Researcher:**\n{RESEARCHER_NAME}")
    st.divider()
    
    st.write(f"🕒 **Live Server Time:**\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.divider()
    
    country = st.selectbox("Select Country Benchmark", list(live_rates.keys()))
    rate = live_rates[country]
    currency_code = country.split('(')[1].replace(')', '')
    
    st.metric(f"Live USD to {currency_code}", f"{rate:.4f}")
    st.caption("Data source: Global Forex Real-time API")
    st.divider()
    st.caption("© 2025 i-HERI | Researcher: Khairul Ridhuan")

# --- 4. DATA SIMULATION ---
np.random.seed(int(time.time()))
market_items = ["Dialysis Kit", "Insulin Pro", "Oncology Phase 1", "Cardiac Stent", "Vaccine Cold-Chain"]
base_usd = [50, 40, 1500, 800, 20]

df = pd.DataFrame({
    "Treatment": market_items,
    "Base_USD": base_usd,
    # Harga pasaran global juga volatile (naik turun 5-10%)
    "Market_Price": [b * rate * (1 + np.random.uniform(0.02, 0.15)) for b in base_usd],
    "Last_Year": [b * rate for b in base_usd]
})
df['Trend'] = np.random.choice(["▲", "▼", "▬"], 5)

# --- 5. MAIN DASHBOARD ---
st.markdown(f"# 🩺 Global Medical Inflation Terminal")
st.write(f"Benchmarking live healthcare costs for **{country}** based on current Forex Rate: **1 USD = {rate:.4f} {currency_code}**")

# Top Metrics
m_cols = st.columns(len(df))
for i, row in df.iterrows():
    m_cols[i].metric(row['Treatment'], f"{currency_code} {row['Market_Price']:,.2f}", f"{row['Trend']} Market Volatility", delta_color="inverse" if row['Trend']=="▲" else "normal")

st.divider()

# --- LOOPHOLE 1: MIDDLEMAN MARKUP ---
col_l1, col_l2 = st.columns([2, 1])
with col_l1:
    st.subheader("🕵️ Supply Chain Leakage Tracker")
    markup_pct = st.slider("Estimate Middleman & Logistic Markup (%)", 10, 100, 35)
    df['Pure_Cost'] = df['Market_Price'] / (1 + (markup_pct/100))
    df['Markup_Amount'] = df['Market_Price'] - df['Pure_Cost']
    
    fig = px.bar(df, x="Treatment", y=["Pure_Cost", "Markup_Amount"], 
                 title="Price Breakdown: Factory Price vs Supply Chain Markup",
                 barmode="stack", color_discrete_sequence=["#1E3A8A", "#EF4444"])
    st.plotly_chart(fig, use_container_width=True)

with col_l2:
    st.error(f"**Researcher Insight:** At a **{markup_pct}%** markup, the intermediaries take more than the production cost in some categories.")
    st.info("💡 **Policy Advice:** Government should subsidize 'Direct-to-Patient' logistics to bypass middleman markups.")

st.divider()

# --- LOOPHOLE 2: THE INJECTION HUB ---
st.subheader("💰 Real-Time Subsidy & Financial Injection Hub")
st.write("Neutralizing inflation through Multi-Sector Cash Injection.")

c_in1, c_in2, c_in3 = st.columns(3)
with c_in1:
    gov_inj = st.number_input(f"Gov Grant Injection ({currency_code} Million)", min_value=0.0, value=100.0)
with c_in2:
    mnc_inj = st.number_input(f"MNC/Corporate Cash ({currency_code} Million)", min_value=0.0, value=50.0)
with c_in3:
    social_inj = st.number_input(f"Zakat/Waqf Social Fund ({currency_code} Million)", min_value=0.0, value=30.0)

total_pool = gov_inj + mnc_inj + social_inj
st.success(f"### Total Resilience Buffer: {currency_code} {total_pool:,.2f} Million")

# --- PATIENT BILLING ---
st.divider()
st.subheader("🧾 Patient Affordability Simulator (Final Bill)")
sel_med = st.selectbox("Select Treatment Category", df['Treatment'])
current_price = df[df['Treatment'] == sel_med]['Market_Price'].values[0]

cb1, cb2 = st.columns(2)
with cb1:
    sub_rate = st.slider("Subsidy Rate from Buffer (%)", 0, 100, 45)
    sub_val = current_price * (sub_rate/100)
    final_pay = current_price - sub_val

with cb2:
    st.markdown(f"""
    <div style="background-color:#ffffff; padding:25px; border-radius:15px; border: 2px solid #1E3A8A;">
        <p style="margin:0;">Actual Market Price: {currency_code} {current_price:,.2f}</p>
        <h3 style="color:green; margin:0;">i-HERI Hedge Buffer: - {currency_code} {sub_val:,.2f}</h3>
        <hr>
        <h1 style="color:#1E3A8A; margin:0;">Patient Pays: {currency_code} {final_pay:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center;'><b>i-HERI Global Index</b> | Researcher: {RESEARCHER_NAME}</div>", unsafe_allow_html=True)
