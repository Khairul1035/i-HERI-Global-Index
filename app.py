import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import requests

# --- 1. ENTERPRISE CONFIGURATION ---
st.set_page_config(page_title="i-HERI | Global Equity Terminal", layout="wide", page_icon="📈")

# CUSTOM CSS: MENGHASILKAN LOOK "BLOOMBERG TERMINAL" (DARK & PROFESSIONAL)
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 6px; border: 1px solid #30363d; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    [data-testid="stMetricValue"] { color: #58a6ff; font-family: 'Courier New', Courier, monospace; font-weight: bold; }
    .header-style { font-size: 28px; font-weight: 800; color: #ffffff; border-bottom: 2px solid #58a6ff; padding-bottom: 10px; font-family: 'Inter', sans-serif; }
    .report-box { background-color: #0d1117; padding: 20px; border-radius: 10px; border: 1px solid #238636; }
    .stSlider > div > div > div > div { background-color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. REAL-TIME DATA FETCHING (LIVE FOREX) ---
@st.cache_data(ttl=3600)
def get_live_rates():
    try:
        # API Tarikan Mata Wang Real-Time
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        return response.json()['rates']
    except:
        # Fallback jika API terganggu
        return {"MYR": 4.45, "SAR": 3.75, "USD": 1.0}

rates = get_live_rates()

# --- 3. SIDEBAR: COMMAND CENTER ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>i-HERI COMMAND CENTER</h2>", unsafe_allow_html=True)
    st.write(f"**Lead Researcher:**\n#### MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL")
    st.divider()
    st.write(f"🕒 **System Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    country = st.selectbox("Benchmark Jurisdiction", ["Malaysia", "Saudi Arabia", "USA"])
    c_code = {"Malaysia": "MYR", "Saudi Arabia": "SAR", "USA": "USD"}[country]
    current_rate = rates[c_code]
    
    st.metric(f"Live Forex Index (USD/{c_code})", f"{current_rate:.4f}")
    st.divider()
    st.caption("Simulation: Internal Use Only | Data Source: Global Forex API")

# --- 4. DATA ENGINE (FIXED KEYBOARD NAMES) ---
treatments = ["Dialysis Kit", "Insulin Pro", "Oncology Phase 1", "Cardiac Stent", "Vaccine Vials"]
base_prices_usd = [50, 40, 1500, 800, 20]

# Simulasi Volatiliti Pasaran (5% ke 15% kenaikan)
np.random.seed(42) # Untuk consistency paparan
volatility_idx = np.random.uniform(1.05, 1.15, len(treatments))
market_prices_local = [b * current_rate * v for b, v in zip(base_prices_usd, volatility_idx)]

# Bina DataFrame dengan penamaan yang konsisten
df = pd.DataFrame({
    "Asset_Class": treatments,
    "Global_Base_USD": base_prices_usd,
    "Local_Price": market_prices_local,
    "Vol_Index": volatility_idx
})

# --- 5. MAIN DASHBOARD ---
st.markdown(f'<div class="header-style">HEALTH EQUITY REAL-TIME INDEX (i-HERI) : {country.upper()}</div>', unsafe_allow_html=True)
st.write("")

# Barisan Metrik (Top Metrics)
m_cols = st.columns(5)
for i, row in df.iterrows():
    # Menghitung % perubahan untuk dipaparkan sebagai delta
    change_pct = (row['Vol_Index'] - 1) * 100
    m_cols[i].metric(
        label=row['Asset_Class'], 
        value=f"{c_code} {row['Local_Price']:,.2f}", 
        delta=f"{change_pct:+.2f}% Vol"
    )

st.divider()

# --- ANALYTICS: INTERMEDIARY LEAKAGE ---
col_l, col_r = st.columns([1.5, 1])

with col_l:
    st.subheader("🕵️ Intermediary Leakage & Supply Chain Analysis")
    markup = st.slider("Estimate Supply Chain Mark-up (%)", 5, 100, 30)
    
    # Pengiraan Leakage
    df['Production_Cost'] = df['Local_Price'] / (1 + (markup/100))
    df['Leakage_Amount'] = df['Local_Price'] - df['Production_Cost']
    
    fig = go.Figure(data=[
        go.Bar(name='Production Cost', x=df['Asset_Class'], y=df['Production_Cost'], marker_color='#1f6feb'),
        go.Bar(name='Supply Chain Leakage', x=df['Asset_Class'], y=df['Leakage_Amount'], marker_color='#da3633')
    ])
    fig.update_layout(
        barmode='stack', 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font_color="#8b949e",
        title_font_size=16,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.subheader("📊 Researcher Interpretation")
    st.markdown(f"""
    <div class="report-box">
    <b>Market Integrity Stress Test:</b><br>
    At a <b>{markup}%</b> markup, approximately 1 in every 3 units of currency spent does not contribute to the medicine's chemical value. 
    <br><br>
    <b>Risk Assessment:</b> {'🔴 CRITICAL' if markup > 30 else '🟢 STABLE'}<br>
    <b>Recommendation:</b> Deploy Social Capital (Waqf/Zakat) as a <b>Direct-Procurement Buffer</b> to neutralize this leakage.
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- CAPITAL INJECTION HUB ---
st.subheader("🏦 Strategic Capital Injection & Resilience Hub")
st.write("Neutralizing inflation through multi-sector liquidity injection (Millions).")

c1, c2, c3 = st.columns(3)
gov_inj = c1.number_input("Government Fiscal Grant", value=50.0)
mnc_inj = c2.number_input("MNC/ESG Resilience Capital", value=20.0)
soc_inj = c3.number_input("Social Equity Capital (Zakat/Waqf)", value=15.0)

# Total dalam nilai sebenar (Jutaan)
total_buffer_val = (gov_inj + mnc_inj + soc_inj) * 1000000
st.info(f"**Total Available Liquidity Buffer:** {c_code} {total_buffer_val:,.2f}")

st.divider()

# --- PATIENT BILLING SIMULATOR ---
st.subheader("🧾 Patient Affordability Simulator")
sel_treatment = st.selectbox("Select Patient Case for Analysis", df['Asset_Class'])
price_point = df[df['Asset_Class'] == sel_treatment]['Local_Price'].values[0]

# Slider untuk apply buffer
hedge_pct = st.slider("Apply i-HERI Social Hedge Buffer (%)", 0, 100, 50)
social_hedge_val = price_point * (hedge_pct/100)
net_payable = price_point - social_hedge_val

cb1, cb2 = st.columns(2)
with cb1:
    st.markdown(f"""
    <div style="padding:30px; border:1px solid #30363d; border-radius:10px; background-color:#161b22;">
    <p style="margin:0; font-size:14px; color:#8b949e;">Market Invoice Price:</p>
    <h3 style="margin:0;">{c_code} {price_point:,.2f}</h3>
    <p style="margin:0; font-size:14px; color:#238636; margin-top:10px;">i-HERI Social Hedge Application:</p>
    <h3 style="margin:0; color:#238636;">- {c_code} {social_hedge_val:,.2f}</h3>
    <hr style="border-color:#30363d;">
    <p style="margin:0; font-size:14px; color:#58a6ff;">Final Amount Payable by Patient:</p>
    <h1 style="color:#58a6ff; margin:0; font-size:45px;">{c_code} {net_payable:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

with cb2:
    if social_hedge_val > 0:
        total_coverage = total_buffer_val / social_hedge_val
    else:
        total_coverage = 0
    st.subheader("🌍 Sustainable Impact Analysis")
    st.write(f"""
    By deploying the current **{c_code} {gov_inj+mnc_inj+soc_inj}M** fund, 
    the system can protect and sustain **{int(total_coverage):,} patients** 
    against medical inflation for this specific asset class.
    """)
    st.progress(min(1.0, total_coverage/100000)) # Progress bar visual

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center; color:#8b949e; font-size:12px;'>Lead Researcher: {RESEARCHER_NAME} | i-HERI Global Index Terminal | Built for Academic & Policy Excellence | © 2025</div>", unsafe_allow_html=True)
