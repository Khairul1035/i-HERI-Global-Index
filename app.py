import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import random

# --- 1. GLOBAL SETTINGS ---
st.set_page_config(page_title="i-HERI | Global Equity Index", layout="wide")
PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- 2. LIVE TICKER DATA (MOCK REAL-TIME) ---
now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

# --- 3. DATABASE: 3 COUNTRIES COMPARISON ---
country_data = {
    "Malaysia": {"Inflation": 14.2, "Currency": "MYR", "Price_Index": 1.0, "Flag": "🇲🇾"},
    "Saudi Arabia": {"Inflation": 10.5, "Currency": "SAR", "Price_Index": 1.5, "Flag": "🇸🇦"},
    "USA": {"Inflation": 18.9, "Currency": "USD", "Price_Index": 4.5, "Flag": "🇺🇸"}
}

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("🌍 i-HERI GLOBAL INDEX")
st.sidebar.markdown(f"**Principal Investigator:**\n{PI_NAME}")
st.sidebar.divider()
st.sidebar.markdown(f"🕒 **System Time:**\n{current_time}")
selected_country = st.sidebar.selectbox("Select Benchmark Country", list(country_data.keys()))

st.sidebar.divider()
nav = st.sidebar.radio("Modules", ["🚀 Live Market Tracker", "💰 Fund Injection Hub", "🔬 The 7 Systemic Loopholes"])

# --- 5. MODULE 1: LIVE MARKET TRACKER ---
if nav == "🚀 Live Market Tracker":
    st.header(f"🚀 Live Medical Market Tracker ({selected_country})")
    st.write(f"Monitoring pharmaceutical price fluctuations in real-time. Benchmark: {selected_country}")

    # Prices Simulation
    meds = ["Insulin Kit", "Dialysis Filters", "Cancer Med A", "Cardiac Stent"]
    base_prices = [150, 250, 5000, 3500]
    
    # Trend Logic (Up/Down)
    trends = [random.choice(["▲", "▼"]) for _ in range(4)]
    fluctuations = [random.uniform(1.0, 5.0) for _ in range(4)]
    
    cols = st.columns(4)
    for i in range(4):
        p_change = fluctuations[i] if trends[i] == "▲" else -fluctuations[i]
        cols[i].metric(meds[i], f"RM {base_prices[i] * country_data[selected_country]['Price_Index']:,.2f}", f"{trends[i]} {fluctuations[i]}%")

    st.divider()
    st.subheader("🌍 Regional Medical Inflation Comparison")
    df_compare = pd.DataFrame([
        {"Country": k, "Inflation (%)": v["Inflation"]} for k, v in country_data.items()
    ])
    fig = px.bar(df_compare, x="Country", y="Inflation (%)", color="Country", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# --- 6. MODULE 2: FUND INJECTION HUB ---
elif nav == "💰 Fund Injection Hub":
    st.header("💰 Subsidy & Cash Injection Hub")
    st.write("Neutralizing Medical Inflation through Strategic Funding.")

    with st.container():
        st.subheader("💳 Step 1: Inject Capital")
        c1, c2, c3 = st.columns(3)
        gov_cash = c1.number_input("Government Subsidy Injection (RM)", value=1000000.0)
        mnc_cash = c2.number_input("MNC Grant Injection (RM)", value=500000.0)
        social_cash = c3.number_input("Islamic Social Finance (Zakat/Waqf) (RM)", value=300000.0)

    total_pool = gov_cash + mnc_cash + social_cash
    st.metric("TOTAL ACCESSIBILITY FUND", f"RM {total_pool:,.2f}")

    st.divider()
    st.subheader("🧾 Step 2: Patient Billing Impact")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        patient_bill = st.number_input("Standard Market Bill (RM)", value=15000.0)
        subsidy_rate = st.slider("Fund Utilization Rate (%)", 0, 100, 40)
    
    subsidy_amt = patient_bill * (subsidy_rate/100)
    final_payable = patient_bill - subsidy_amt

    with col_b2:
        st.markdown(f"""
        ### **Billing Result**
        - Gross Bill: RM {patient_bill:,.2f}
        - Total Subsidy Applied: -RM {subsidy_amt:,.2f}
        - **Net Patient Payable: RM {final_payable:,.2f}**
        """)
        if final_payable > (0.5 * patient_bill):
            st.error("⚠️ CRITICAL: Patient burden is still high. Increase Social Capital injection.")
        else:
            st.success("✅ STABLE: Healthcare is affordable for the patient.")

# --- 7. MODULE 3: THE 7 LOOPHOLES ---
elif nav == "🔬 The 7 Systemic Loopholes":
    st.header("🔬 7 Systemic Loopholes Burdensome to Citizens")
    st.write("As identified by PI Mohd Khairul Ridhuan (2025). These hidden costs increase medical inflation.")

    loopholes = [
        ("Currency Volatility", "Meds imported in USD. Local currency drops spike prices instantly."),
        ("Middlemen Markups", "Multi-layered distribution channels take 10-20% margin each."),
        ("Late Fund Disbursement", "Late government payments force patients to pay upfront."),
        ("Over-Prescription", "Preference for expensive brand names over generic alternatives."),
        ("Admin Bureaucracy", "15% of funds leaked into administrative overheads."),
        ("Maintenance Gaps", "Broken hospital equipment leads to high outsource costs."),
        ("Defensive Medicine", "Unnecessary tests to avoid legal risks, paid by patients.")
    ]

    for title, desc in loopholes:
        with st.expander(f"🔴 {title}"):
            st.write(desc)
            st.slider(f"Estimated Impact on Inflation for {title} (%)", 0, 10, 5)

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center;'><b>i-HERI Project</b> | Principal Investigator: {PI_NAME}</div>", unsafe_allow_html=True)
st.caption("Benchmark Data for Educational Purposes only: Malaysia, Saudi, USA.")
