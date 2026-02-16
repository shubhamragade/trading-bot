# 🤖 Binance Alpha | AI Trading Terminal

A high-maturity, recruiter-ready trading bot for the **Binance Futures Testnet (USDT-M)**. This project demonstrates advanced skills in **FastAPI**, **Streamlit**, **Manual Cryptographic Signing**, and **Conversational AI / Intent Parsing**.

## ⚡ Key Highlights (Recruiter Scorecard)

- 🦾 **AI Chatbot Interface**: Replaced generic forms with an interactive, conversational terminal.
- 🔐 **Zero-Library API Client**: Implemented manual **HMAC-SHA256** request signing to demonstrate deep protocol knowledge.
- 🌐 **Distributed Architecture**: Multi-process setup with a **FastAPI** backend and **Streamlit** frontend.
- 📉 **Real-Time Telemetry**: Live BTC price and USDT account balance tracking via REST polling.
- 🛡️ **Defensive Engineering**: Triple-layer validation (Pydantic models, pre-API logic, and exchange error handling).
- 🧪 **Safe Demo Mode**: Built-in **Simulation Mode** allows for a full UI walkthrough without requiring real API keys.

---

## 🏗️ Architecture

```text
trading_bot/
├── bot/
│   ├── api.py           # FastAPI Backend (REST API)
│   ├── st_app.py        # Streamlit Frontend (Conversational UI)
│   ├── parser.py        # AI Intent Parser (Natural Language Extraction)
│   ├── client.py        # Manual REST client with HMAC-SHA256 signing
│   ├── orders.py        # Transaction logic & response formatting
│   ├── validators.py    # Multi-layered input validation
│   └── logging_config.py# Centralized structured logging
├── logs/                # Trade execution logs (trading.log)
├── README.md            # You are here
├── requirements.txt     # Dependency list
└── .env.example         # Template for secure credentials
```

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/shubhamragade/trading-bot.git
cd trading_bot
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file from the example:
```bash
cp .env.example .env
```
Add your **Binance Futures Testnet** keys:
```env
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
SIMULATION_MODE=False
```

### 3. Execution
You need to run both the backend and the frontend:

**Terminal 1 (Backend API):**
```bash
uvicorn bot.api:app --reload
```

**Terminal 2 (AI Dashboard):**
```bash
streamlit run bot/st_app.py
```

---

## 🤖 Interaction Examples

Once the dashboard is open, try these natural language commands:

- **Market Orders**: *"Go long 0.002 BTC"* or *"Short 0.5 ETH at market"*
- **Limit Orders**: *"Buy 0.01 BTC at 45000"* or *"Limit sell 1 SOL at 150"*
- **Stop-Limit Orders**: *"Stop limit buy 0.005 BTC price 111000 trigger 110000"*

---

## 🛡️ Stability & Quality
- **Type Hinting**: Fully typed codebase for IDE support and maintenance.
- **Structured Logging**: All trades, connections, and rejections are logged in `logs/trading.log`.
- **Validation**: Prevents negative quantities, invalid prices, and notional floor violations.

---
Developed as a demonstration of high-level Python Engineering & Fintech Innovation.
