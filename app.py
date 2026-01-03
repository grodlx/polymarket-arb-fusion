import streamlit as st
import pandas as pd
import plotly.express as px
import time
import numpy as np
from datetime import datetime
from utils.gas_calc import calculate_gas_adjusted_profit
from engine.fusion import get_market_correlations, detect_anomalies

# Konfigurace
st.set_page_config(page_title="Polymarket Fusion Arb", layout="wide")

if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []
if 'price_history' not in st.session_state:
    st.session_state.price_history = pd.DataFrame(columns=['BTC', 'ETH', 'SOL', 'POL'])

# --- SIDEBAR ---
st.sidebar.header("⚙️ Bot Configuration")
target_vol = st.sidebar.number_input("Target Volume (USD)", value=500)
min_edge = st.sidebar.slider("Min. Edge (%)", 0.1, 3.0, 0.5)
matic_p = st.sidebar.number_input("MATIC Price (USD)", value=0.70)

# --- SIMULACE DAT (MOCK) ---
def get_live_data():
    # V reálu zde bude requests.get("https://clob.polymarket.com/book?token_id=...")
    y_p = 0.485 + np.random.uniform(-0.02, 0.02)
    n_p = 0.490 + np.random.uniform(-0.02, 0.02)
    return y_p, n_p

# --- MAIN LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🚀 Live Scanner")
    y, n = get_live_data()
    total = y + n
    gross_profit_pct = (1 - total) * 100
    
    gas_info = calculate_gas_adjusted_profit(gross_profit_pct, target_vol, matic_price=matic_p)
    
    st.metric("Gross Spread", f"{total:.4f}", f"{gross_profit_pct:.2f}%")
    st.metric("Net Profit (After Gas)", f"${gas_info['net_profit']:.2f}")
    
    if gas_info['is_viable'] and gross_profit_pct > min_edge:
        st.success("MATCH: Arbitrage Opportunity Found!")
        if st.button("Manual Override Execute"):
            st.session_state.trade_history.append({
                "Time": datetime.now(), "Type": "ARB", "Profit": gas_info['net_profit']
            })

with col2:
    st.subheader("🔗 Correlation Fusion")
    # Simulace přidávání dat do historie
    new_prices = np.random.normal(0, 0.01, 4).cumsum() + [60000, 2400, 140, 0.7]
    new_df = pd.DataFrame([new_prices], columns=['BTC', 'ETH', 'SOL', 'POL'])
    st.session_state.price_history = pd.concat([st.session_state.price_history, new_df]).tail(50)
    
    corr = get_market_correlations(st.session_state.price_history)
    fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r')
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- ANOMALIES & HISTORY ---
c3, c4 = st.columns([1, 1])
with c3:
    st.write("Anomalies (Z-Score)")
    z = detect_anomalies(st.session_state.price_history)
    if z is not None:
        st.bar_chart(z)

with c4:
    st.write("Trade Execution Log")
    if st.session_state.trade_history:
        st.table(pd.DataFrame(st.session_state.trade_history).tail(5))

time.sleep(2)
st.rerun()
