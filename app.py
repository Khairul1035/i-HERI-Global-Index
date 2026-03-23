import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import requests

# --- 1. ENTERPRISE CONFIG ---
st.set_page_config(page_title="i-HERI | Global Health Equity Terminal", layout="wide")

# CUSTOM CSS UNTUK LOOK KORPORAT (DARK/CLEAN LOOK)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #fafafa; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 5px; border: 1px solid #30363d; }
    .header-style { font-size: 25px; font-weight: bold; color: #58a6ff; border-bottom: 2px solid #30363d; padding-bottom: 10px; }
    .report-box { background-color: #161b22; padding: 20px; border-radius: 8px; border-left: 5px solid #238636; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LIVE DATA FETCHING ---
@st.cache_data(ttl=3600)
def get_live_rates():
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        return response.json()['rates']
    except:
        return {"MYR": 4.45, "SAR": 3.75, "USD": 1.0}

rates = get_live_rates()

# --- 3. SIDEBAR (CONTROL PANEL) ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>i-HERI COMMAND CENTER</h2>", unsafe_allow_html=True)
    st.write(f"**Lead Researcher:**\nMOHD KHAIRUL RIDHUAN BIN MOHD FADZIL")
    st.divider()
    st.write(f"🕒 **System Live:** {datetime.now().strftime('%H:%M:%S')}")
    
    country = st.selectbox("Benchmark Jurisdiction", ["Malaysia", "Saudi Arabia", "USA"])
    c_code = {"Malaysia": "MYR", "Saudi Arabia": "SAR", "USA": "USD"}[country]
    current_rate = rates[c_code]
    
    st.metric(f"Live USD/{c_code}", f"{current_rate:.4f}")
    st.divider()
    st.caption("INTERNAL SIMULATION FOR EDUCATIONAL PURPOSES ONLY")

# --- 4. DATA ENGINE (STRESS TEST MODELING) ---
treatments = ["Dialysis Kit", "Insulin Pro", "Oncology Phase 1", "Cardiac Stent", "Vaccine Vials"]
base_prices = [50, 40, 1500, 800, 20]

# Simulasi Volatiliti
volatility = np.random.uniform(0.95, 1.15, len(treatments))
market_prices = [b * current_rate * v for b, v in zip(base_prices, volatility)]

df = pd.DataFrame({
    "Asset Class": treatments,
    "Global Base (USD)": base_prices,
    "Local Market Price": market_prices,
    "Volatility Index": volatility
})

# --- 5. MAIN DASHBOARD (TERMINAL VIEW) ---
st.markdown(f'<div class="header-style">HEALTH EQUITY REAL-TIME INDEX (i-HERI) - {country.upper()}</div>', unsafe_allow_html=True)
st.write("")

# Metrics Row
cols = st.columns(5)
for i, row in df.iterrows():
    cols[i].metric(row['Asset Class'], f"{c_code} {row['Local_Market_Price']:,.2f}", f"{((row['Volatility_Index']-1)*100):+.2f}%")

st.divider()

# --- ANALYTICS: INFLATION & LEAKAGE ---
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("📊 Systemic Supply Chain Analysis")
    markup = st.slider("Intermediary Mark-up & Logistics Fee (%)", 5, 100, 30)
    df['Pure Cost'] = df['Local Market Price'] / (1 + (markup/100))
    df['Leakage'] = df['Local Market Price'] - df['Pure Cost']
    
    fig = go.Figure(data=[
        go.Bar(name='Production Cost', x=df['Asset Class'], y=df['Pure Cost'], marker_color='#1f6feb'),
        go.Bar(name='Supply Chain Leakage', x=df['Asset Class'], y=df['Leakage'], marker_color='#da3633')
    ])
    fig.update_layout(barmode='stack', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🔍 Researcher Insight")
    st.markdown(f"""
    <div class="report-box">
    <b>Scenario Stress Test:</b><br>
    At a {markup}% markup, the economy is losing billions in <b>non-value-added logistics</b>. 
    <br><br>
    <b>Equity Risk Level:</b> {'🔴 HIGH' if markup > 30 else '🟢 MANAGEABLE'}<br>
    <b>Recommendation:</b> Shift Zakat/Waqf capital towards <b>Sovereign Direct Procurement</b> to eliminate middleman margins.
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- FINANCIAL INJECTION & BILLING ---
st.subheader("🏦 Strategic Capital Injection Hub")
c1, c2, c3 = st.columns(3)
gov = c1.number_input("Government Fiscal Grant (Millions)", value=50.0)
corp = c2.number_input("MNC/ESG Capital (Millions)", value=20.0)
social = c3.number_input("Social Capital (Waqf/Zakat) (Millions)", value=15.0)

total_buffer = (gov + corp + social) * 1000000
st.info(f"**Total Liquidity Buffer Available:** {c_code} {total_buffer:,.2f}")

st.divider()

# --- THE OUTCOME ---
st.subheader("🧾 Patient Affordability Simulator")
sel_item = st.selectbox("Select Patient Case", treatments)
actual_p = df[df['Asset Class'] == sel_item]['Local Market Price'].values[0]

# Slider untuk apply buffer
buffer_applied = st.slider("Apply i-HERI Hedge Buffer (%)", 0, 100, 50)
subsidy = actual_p * (buffer_applied/100)
final_bill = actual_p - subsidy

col_bill, col_impact = st.columns(2)
with col_bill:
    st.markdown(f"""
    <div style="padding:30px; border:1px solid #30363d; border-radius:10px;">
    <p>Market Invoice Price: {c_code} {actual_p:,.2f}</p>
    <p style="color:#238636;">i-HERI Social Hedge: - {c_code} {subsidy:,.2f}</p>
    <hr>
    <h1 style="color:#58a6ff; margin:0;">Payable: {c_code} {final_bill:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

with col_impact:
    capacity = total_buffer / subsidy if subsidy > 0 else 0
    st.subheader("🌍 Scalability Impact")
    st.write(f"With the current injection of **{c_code} {gov+corp+social}M**, this system can protect **{int(capacity):,}** patients from medical inflation for this specific treatment.")

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center; color:#8b949e;'>Researcher: {RESEARCHER_NAME} | Global Equity Resilience Index | © 2025</div>", unsafe_allow_html=True)
