# Binance Futures Trading Bot (USDT-M)

A professional, recruiter-ready Python application for placing orders on the Binance Futures Testnet. This project demonstrates clean architecture, defensive programming, and a user-centric design.

## Features

- **Standard CLI**: Place orders via command-line arguments.
- **Interactive Mode**: Guided terminal experience with prompts and confirmations.
- **Web Dashboard**: Lightweight browser-based interface for order placement.
- **Order Types**: Support for **MARKET**, **LIMIT**, and **STOP_LIMIT** orders.
- **Security**: API keys are securely managed via environment variables.
- **Error Handling**: Graceful handling of API errors, network failures, and invalid inputs.
- **Logging**: Structured logs for all API interactions in `trading_bot/logs/trading.log`.

## Architecture

The project follows a modular structure to ensure maintainability and readability:

- `bot/client.py`: Wrapper for the Binance API client.
- `bot/orders.py`: Core logic for order placement and response formatting.
- `bot/validators.py`: Input validation layer for defensive programming.
- `bot/logging_config.py`: Centralized logging configuration.
- `bot/cli.py`: CLI entry point (Standard & Interactive).
- `bot/web_ui.py`: Flask-based web server.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd trading_bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   - Rename `.env.example` to `.env`.
   - Add your Binance Futures Testnet API Key and Secret.
   ```env
   BINANCE_API_KEY=your_api_key
   BINANCE_API_SECRET=your_secret
   ```

## Usage Examples

### 1. Standard CLI Mode
Ensure you are in the `trading_bot` root directory.
```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### 2. Interactive Mode (Recommended)
```bash
python -m bot.cli --interactive
```

### 3. Web UI Mode (FastAPI + Streamlit)

**Start the Backend**:
```bash
uvicorn bot.api:app --reload
```

**Start the Frontend**:
```bash
streamlit run bot/st_app.py
```
Then open the Streamlit URL provided in the terminal (usually `http://localhost:8501`).

## Error Handling & Validation
The bot performs several checks before sending orders:
- **FastAPI Validation**: Uses Pydantic to ensure data types are correct.
- **Pre-API Logic**: Ensures quantity and prices are positive.
- **Binance API Errors**: Displays specific messages for exchange-side failures.

## Architecture
- `bot/api.py`: FastAPI backend server.
- `bot/st_app.py`: Streamlit frontend dashboard.
- `bot/client.py`: Binance connection wrapper.
- `bot/orders.py`: Transaction logic.
- `bot/validators.py`: Input safety checks.
