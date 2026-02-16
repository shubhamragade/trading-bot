import streamlit as st
import requests
import json
import os
import sys
import time
from dotenv import load_dotenv

# Fix path for Streamlit when running from subfolder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.parser import CommandParser

load_dotenv()

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Alpha-Bot | AI Terminal",
    page_icon="🤖",
    layout="wide",
)

# Premium Dark Mode Logic
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at top right, #1a1c2c, #0d0e12);
    }
    
    /* Header Styling */
    .stHeader {
        background: transparent;
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-family: 'Courier New', Courier, monospace;
        color: #00ffcc !important;
        font-weight: 700;
    }
    
    /* Chat Message Styling */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px !important;
        margin-bottom: 8px !important;
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #111217;
    }
</style>
""", unsafe_allow_html=True)

# --- BACKEND API SETTINGS ---
API_BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
IS_SIMULATION = os.getenv("SIMULATION_MODE", "False").lower() == "true"

# --- HELPER FUNCTIONS ---
def get_account_data():
    try:
        response = requests.get(f"{API_BASE_URL}/account", timeout=3)
        if response.status_code == 200:
            return response.json()
    except: pass
    return {"wallet_balance": "0.00", "assets_count": 0}

def get_symbol_price(symbol):
    try:
        response = requests.get(f"{API_BASE_URL}/price/{symbol}", timeout=3)
        if response.status_code == 200:
            return response.json().get("price", "0.00")
    except: pass
    return "0.00"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00ffcc;'>Alpha ⚡ Bot</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Portfolio Snapshot
    st.subheader("📊 Portfolio Status")
    acc = get_account_data()
    st.metric("USDT Balance", f"${float(acc['wallet_balance']):,.2f}")
    
    # Market Info
    st.subheader("🌎 Market Info")
    btc_price = get_symbol_price("BTCUSDT")
    st.metric("BTC Price", f"${float(btc_price):,.2f}")
    
    st.markdown("---")
    env_label = "🟡 SIMULATION" if IS_SIMULATION else "🟢 REAL TESTNET"
    st.markdown(f"**Runtime**: `{env_label}`")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- CHAT INTERFACE ---
st.title("🤖 AI Trading Terminal")
st.markdown("*Talk to your bot. Execute professional trades in seconds.*")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to **Alpha Terminal**. I am ready to execute your orders.\n\nYou can say things like:\n- `Buy 0.01 BTC at market`\n- `Limit sell 0.5 ETH at 2500`"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Command: e.g. Buy 0.01 BTC"):
    # User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI Processing
    with st.chat_message("assistant"):
        with st.spinner("Processing Strategy..."):
            intent = CommandParser.parse(prompt)
            
            if intent:
                st.info(f"📍 **Target Identified**: {intent['side']} {intent['quantity']} {intent['symbol']} ({intent['type']})")
                
                # Execution
                try:
                    res = requests.post(f"{API_BASE_URL}/place_order", json=intent, timeout=10)
                    data = res.json()
                    
                    if res.status_code == 200:
                        success_msg = f"🛡️ **Execution Successful**\n\n```\n{data.get('details')}\n```"
                        st.success(success_msg)
                        st.session_state.messages.append({"role": "assistant", "content": success_msg})
                    else:
                        err_msg = f"❌ **Exchange Rejection**: {data.get('detail', 'Network failure')}"
                        st.error(err_msg)
                        st.session_state.messages.append({"role": "assistant", "content": err_msg})
                except Exception as e:
                    sys_err = f"⚠️ **Critical System Error**: {str(e)}"
                    st.error(sys_err)
                    st.session_state.messages.append({"role": "assistant", "content": sys_err})
            else:
                fail_msg = "⚠️ **Invalid Input**: I couldn't parse that command. Please use the format: `[Action] [Qty] [Symbol] at [Price/Market]`."
                st.warning(fail_msg)
                st.session_state.messages.append({"role": "assistant", "content": fail_msg})

# Scroll to bottom logic is automatic in modern Streamlit chat_input
