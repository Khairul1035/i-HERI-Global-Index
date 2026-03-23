import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import requests

# =========================================================
# 1. PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="i-HERI | Global Equity Terminal",
    layout="wide",
    page_icon="📈"
)

RESEARCHER_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"
CURRENT_YEAR = datetime.now().year

# =========================================================
# 2. HIGH-CONTRAST CSS
# =========================================================
st.markdown("""
<style>
    /* ===============================
       GLOBAL APP
    =============================== */
    .stApp {
        background-color: #0D1117 !important;
        color: #F0F6FC !important;
    }

    .main {
        background-color: #0D1117 !important;
        color: #F0F6FC !important;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
        color: #F0F6FC !important;
    }

    /* Semua teks biasa */
    p, span, div, label, li {
        color: #E6EDF3 !important;
    }

    /* Heading */
    h1, h2, h3, h4, h5, h6 {
        color: #F8FAFC !important;
    }

    /* ===============================
       SIDEBAR
    =============================== */
    section[data-testid="stSidebar"] {
        background-color: #0B1220 !important;
        border-right: 1px solid #30363D;
    }

    section[data-testid="stSidebar"] * {
        color: #F0F6FC !important;
    }

    /* ===============================
       METRICS
    =============================== */
    div[data-testid="stMetric"] {
        background-color: #111827 !important;
        border: 1px solid #30363D !important;
        border-radius: 10px !important;
        padding: 14px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.28) !important;
    }

    [data-testid="stMetricLabel"] {
        color: #C9D1D9 !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-family: 'Courier New', monospace !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #3FB950 !important;
        font-weight: 700 !important;
    }

    /* ===============================
       INPUT LABELS
    =============================== */
    .stSelectbox label,
    .stSlider label,
    .stNumberInput label,
    .stTextInput label,
    .stTextArea label,
    .stDateInput label,
    .stTimeInput label,
    .stMultiSelect label {
        color: #F0F6FC !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }

    /* ===============================
       INPUT BOXES
    =============================== */
    div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        color: #F0F6FC !important;
        border: 1px solid #30363D !important;
    }

    div[data-baseweb="select"] * {
        color: #F0F6FC !important;
    }

    .stNumberInput input,
    .stTextInput input,
    .stTextArea textarea {
        background-color: #111827 !important;
        color: #F0F6FC !important;
        border: 1px solid #30363D !important;
    }

    /* ===============================
       SLIDER
    =============================== */
    .stSlider [data-baseweb="slider"] * {
        color: #F0F6FC !important;
    }

    .stSlider > div > div > div > div {
        background-color: #58A6FF !important;
    }

    /* ===============================
       CAPTION / MUTED TEXT
    =============================== */
    .stCaption, small {
        color: #9AA4B2 !important;
        opacity: 1 !important;
    }

    /* ===============================
       INFO / ALERT BOX
    =============================== */
    div[data-testid="stInfo"] {
        background-color: #0F2747 !important;
        border: 1px solid #1F6FEB !important;
        color: #F0F6FC !important;
        border-radius: 8px !important;
    }

    div[data-testid="stInfo"] * {
        color: #F0F6FC !important;
    }

    /* ===============================
       DATAFRAME
    =============================== */
    div[data-testid="stDataFrame"] {
        border: 1px solid #30363D !important;
        border-radius: 8px !important;
    }

    /* ===============================
       BUTTON
    =============================== */
    .stDownloadButton button,
    .stButton button {
        background-color: #1F6FEB !important;
        color: #FFFFFF !important;
        border: 1px solid #1F6FEB !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }

    /* ===============================
       CUSTOM CLASSES
    =============================== */
    .header-style {
        font-size: 28px;
        font-weight: 800;
        color: #FFFFFF !important;
        border-bottom: 2px solid #58A6FF;
        padding-bottom: 10px;
        font-family: 'Inter', sans-serif;
        margin-bottom: 0.6rem;
    }

    .report-box {
        background-color: #0F172A;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #238636;
        color: #F0F6FC !important;
        line-height: 1.7;
    }

    .report-box * {
        color: #F0F6FC !important;
    }

    .summary-box {
        background-color: #0F172A;
        border: 1px solid #30363D;
        border-left: 4px solid #58A6FF;
        border-radius: 10px;
        padding: 16px 18px;
        color: #F0F6FC !important;
        margin-bottom: 12px;
    }

    .summary-box * {
        color: #F0F6FC !important;
    }

    .info-box {
        background-color: #0F2747;
        border: 1px solid #1F6FEB;
        border-radius: 8px;
        padding: 14px 16px;
        color: #F0F6FC !important;
        font-weight: 700;
    }

    .invoice-box {
        padding: 30px;
        border: 1px solid #30363D;
        border-radius: 10px;
        background-color: #111827;
        color: #F0F6FC !important;
    }

    .invoice-label {
        margin: 0;
        font-size: 14px;
        color: #C9D1D9 !important;
    }

    .invoice-main {
        margin: 0;
        color: #FFFFFF !important;
        font-size: 20px;
        font-weight: 700;
    }

    .invoice-green-label {
        margin: 0;
        font-size: 14px;
        color: #3FB950 !important;
        margin-top: 10px;
    }

    .invoice-green-value {
        margin: 0;
        color: #3FB950 !important;
        font-size: 20px;
        font-weight: 700;
    }

    .invoice-blue-label {
        margin: 0;
        font-size: 14px;
        color: #58A6FF !important;
    }

    .invoice-final {
        margin: 0;
        color: #58A6FF !important;
        font-size: 42px;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. LIVE FOREX DATA
# =========================================================
@st.cache_data(ttl=3600)
def get_live_rates():
    fallback_rates = {"MYR": 4.45, "SAR": 3.75, "USD": 1.0}
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
        response.raise_for_status()
        data = response.json()
        rates = data.get("rates", fallback_rates)
        return rates
    except Exception:
        return fallback_rates

rates = get_live_rates()

# =========================================================
# 4. SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("<h2 style='color:#58A6FF;'>i-HERI COMMAND CENTER</h2>", unsafe_allow_html=True)
    st.markdown(f"**Lead Researcher:**  \n#### {RESEARCHER_NAME}")
    st.divider()

    st.write(f"🕒 **System Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    country = st.selectbox("Benchmark Jurisdiction", ["Malaysia", "Saudi Arabia", "USA"])
    c_code = {"Malaysia": "MYR", "Saudi Arabia": "SAR", "USA": "USD"}[country]
    current_rate = rates.get(c_code, 1.0)

    st.metric(f"Live Forex Index (USD/{c_code})", f"{current_rate:.4f}")
    st.divider()
    st.caption("Simulation: Internal Use Only | Data Source: Global Forex API")

# =========================================================
# 5. DATA ENGINE
# =========================================================
treatments = [
    "Dialysis Kit",
    "Insulin Pro",
    "Oncology Phase 1",
    "Cardiac Stent",
    "Vaccine Vials"
]

base_prices_usd = [50, 40, 1500, 800, 20]

np.random.seed(42)
volatility_idx = np.random.uniform(1.05, 1.15, len(treatments))
market_prices_local = [b * current_rate * v for b, v in zip(base_prices_usd, volatility_idx)]

df = pd.DataFrame({
    "Asset_Class": treatments,
    "Global_Base_USD": base_prices_usd,
    "Local_Price": market_prices_local,
    "Vol_Index": volatility_idx
})

# =========================================================
# 6. HEADER + EXECUTIVE SUMMARY
# =========================================================
st.markdown(
    f'<div class="header-style">HEALTH EQUITY REAL-TIME INDEX (i-HERI): {country.upper()}</div>',
    unsafe_allow_html=True
)

avg_vol = (df["Vol_Index"].mean() - 1) * 100
highest_asset = df.loc[df["Local_Price"].idxmax(), "Asset_Class"]
highest_price = df["Local_Price"].max()

st.markdown(f"""
<div class="summary-box">
    <b>Executive Summary:</b><br>
    Current benchmark jurisdiction is <b>{country}</b>. Average market volatility across tracked medical assets is
    <b>{avg_vol:.2f}%</b>. The highest priced asset in the present simulation is <b>{highest_asset}</b> at
    <b>{c_code} {highest_price:,.2f}</b>. This terminal is designed to estimate inflation pressure,
    supply-chain leakage, and affordability intervention capacity in real time.
</div>
""", unsafe_allow_html=True)

# =========================================================
# 7. TOP METRICS
# =========================================================
m_cols = st.columns(5)
for i, row in df.iterrows():
    change_pct = (row["Vol_Index"] - 1) * 100
    m_cols[i].metric(
        label=row["Asset_Class"],
        value=f"{c_code} {row['Local_Price']:,.2f}",
        delta=f"{change_pct:+.2f}% Vol"
    )

st.divider()

# =========================================================
# 8. INTERMEDIARY LEAKAGE ANALYSIS
# =========================================================
col_l, col_r = st.columns([1.6, 1])

with col_l:
    st.subheader("🕵️ Intermediary Leakage & Supply Chain Analysis")
    markup = st.slider("Estimate Supply Chain Mark-up (%)", 5, 100, 30)

    df["Production_Cost"] = df["Local_Price"] / (1 + (markup / 100))
    df["Leakage_Amount"] = df["Local_Price"] - df["Production_Cost"]
    df["Leakage_Rate_Pct"] = (df["Leakage_Amount"] / df["Local_Price"]) * 100

    fig = go.Figure(data=[
        go.Bar(
            name="Production Cost",
            x=df["Asset_Class"],
            y=df["Production_Cost"],
            marker_color="#1F6FEB"
        ),
        go.Bar(
            name="Supply Chain Leakage",
            x=df["Asset_Class"],
            y=df["Leakage_Amount"],
            marker_color="#F85149"
        )
    ])

    fig.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F0F6FC", size=13),
        legend=dict(font=dict(color="#F0F6FC")),
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(title="", tickfont=dict(color="#F0F6FC")),
        yaxis=dict(title="Amount", tickfont=dict(color="#F0F6FC"))
    )

    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.subheader("📊 Researcher Interpretation")

    if markup <= 20:
        risk_status = "🟢 LOW RISK"
        risk_note = "Supply chain distortion remains relatively contained."
    elif markup <= 35:
        risk_status = "🟡 MODERATE RISK"
        risk_note = "Leakage is becoming material and requires targeted intervention."
    else:
        risk_status = "🔴 HIGH RISK"
        risk_note = "A large portion of patient expenditure is diverted away from therapeutic value."

    avg_leakage = df["Leakage_Amount"].mean()

    st.markdown(f"""
    <div class="report-box">
        <b>Market Integrity Stress Test:</b><br>
        At a <b>{markup}%</b> markup, the average estimated non-therapeutic leakage per asset is
        <b>{c_code} {avg_leakage:,.2f}</b>.<br><br>

        <b>Risk Assessment:</b> {risk_status}<br>
        <b>Interpretation:</b> {risk_note}<br><br>

        <b>Recommendation:</b> Deploy Social Capital (Waqf/Zakat) and direct procurement mechanisms
        as a <b>protective affordability buffer</b> to reduce inflation transmission into final patient billing.
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================================================
# 9. CAPITAL INJECTION HUB
# =========================================================
st.subheader("🏛️ Strategic Capital Injection & Resilience Hub")
st.write("Neutralizing inflation through multi-sector liquidity injection (Millions).")

c1, c2, c3 = st.columns(3)
gov_inj = c1.number_input("Government Fiscal Grant", min_value=0.0, value=50.0, step=5.0)
mnc_inj = c2.number_input("MNC/ESG Resilience Capital", min_value=0.0, value=20.0, step=5.0)
soc_inj = c3.number_input("Social Equity Capital (Zakat/Waqf)", min_value=0.0, value=15.0, step=5.0)

total_buffer_val = (gov_inj + mnc_inj + soc_inj) * 1_000_000

st.markdown(
    f"""
    <div class="info-box">
        Total Available Liquidity Buffer: {c_code} {total_buffer_val:,.2f}
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# 10. PATIENT AFFORDABILITY SIMULATOR
# =========================================================
st.subheader("🧾 Patient Affordability Simulator")

sel_treatment = st.selectbox("Select Patient Case for Analysis", df["Asset_Class"])
price_point = df.loc[df["Asset_Class"] == sel_treatment, "Local_Price"].values[0]

hedge_pct = st.slider("Apply i-HERI Social Hedge Buffer (%)", 0, 100, 50)
social_hedge_val = price_point * (hedge_pct / 100)
net_payable = max(0, price_point - social_hedge_val)

cb1, cb2 = st.columns(2)

with cb1:
    st.markdown(f"""
    <div class="invoice-box">
        <p class="invoice-label">Market Invoice Price:</p>
        <h3 class="invoice-main">{c_code} {price_point:,.2f}</h3>

        <p class="invoice-green-label">i-HERI Social Hedge Application:</p>
        <h3 class="invoice-green-value">- {c_code} {social_hedge_val:,.2f}</h3>

        <hr style="border-color:#30363D; margin:16px 0;">

        <p class="invoice-blue-label">Final Amount Payable by Patient:</p>
        <h1 class="invoice-final">{c_code} {net_payable:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

with cb2:
    total_coverage = int(total_buffer_val / social_hedge_val) if social_hedge_val > 0 else 0

    st.subheader("🌍 Sustainable Impact Analysis")
    st.write(
        f"By deploying the current **{c_code} {gov_inj + mnc_inj + soc_inj:.1f}M** fund, "
        f"the system can protect approximately **{total_coverage:,} patients** "
        f"against inflation pressure for this selected asset class."
    )
    st.progress(min(1.0, total_coverage / 100000))

st.divider()

# =========================================================
# 11. DETAILED ANALYTICS TABLE
# =========================================================
st.subheader("🧮 Detailed Asset Diagnostics")

display_df = df.copy()
display_df["Global_Base_USD"] = display_df["Global_Base_USD"].map(lambda x: f"{x:,.2f}")
display_df["Local_Price"] = display_df["Local_Price"].map(lambda x: f"{x:,.2f}")
display_df["Production_Cost"] = display_df["Production_Cost"].map(lambda x: f"{x:,.2f}")
display_df["Leakage_Amount"] = display_df["Leakage_Amount"].map(lambda x: f"{x:,.2f}")
display_df["Vol_Index"] = display_df["Vol_Index"].map(lambda x: f"{x:.4f}")
display_df["Leakage_Rate_Pct"] = df["Leakage_Rate_Pct"].map(lambda x: f"{x:.2f}%")

st.dataframe(display_df, use_container_width=True)

# =========================================================
# 12. CSV DOWNLOAD
# =========================================================
csv_df = df.copy()
csv_df["Country"] = country
csv_df["Currency_Code"] = c_code
csv_df["Markup_Assumption_Pct"] = markup
csv_df["Government_Grant_Million"] = gov_inj
csv_df["MNC_ESG_Capital_Million"] = mnc_inj
csv_df["Social_Equity_Capital_Million"] = soc_inj
csv_df["Selected_Treatment"] = sel_treatment
csv_df["Selected_Treatment_Market_Price"] = price_point
csv_df["Hedge_Buffer_Pct"] = hedge_pct
csv_df["Social_Hedge_Value"] = social_hedge_val
csv_df["Net_Payable"] = net_payable

csv_bytes = csv_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Analysis CSV",
    data=csv_bytes,
    file_name=f"i_heri_analysis_{country.lower().replace(' ', '_')}.csv",
    mime="text/csv"
)

# =========================================================
# 13. FOOTER
# =========================================================
st.divider()
st.markdown(
    f"""
    <div style='text-align:center; color:#9AA4B2; font-size:12px;'>
        Lead Researcher: {RESEARCHER_NAME} | i-HERI Global Index Terminal |
        Built for Academic & Policy Excellence | © {CURRENT_YEAR}
    </div>
    """,
    unsafe_allow_html=True
)
