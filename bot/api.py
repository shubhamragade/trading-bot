import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from bot.client import BinanceClient
from bot.orders import OrderManager
from bot.validators import InputValidator
from bot.logging_config import setup_logging

# Initialize logging
setup_logging()

app = FastAPI(title="Binance Trading Bot API")

class OrderRequest(BaseModel):
    symbol: str = Field(..., example="BTCUSDT")
    side: str = Field(..., example="BUY")
    order_type: str = Field(..., alias="type", example="MARKET")
    quantity: float = Field(..., gt=0)
    price: Optional[float] = None
    stop_price: Optional[float] = None

@app.post("/place_order")
async def place_order(order: OrderRequest):
    try:
        # Validate inputs using existing validator logic
        clean_data = InputValidator.validate_inputs(
            order.symbol,
            order.side,
            order.order_type,
            order.quantity,
            order.price,
            order.stop_price
        )
        
        # Connect & Place Order
        client_wrapper = BinanceClient()
        order_manager = OrderManager(client_wrapper)
        
        response = None
        if clean_data['type'] == 'MARKET':
            response = order_manager.place_market_order(
                clean_data['symbol'], clean_data['side'], clean_data['quantity']
            )
        elif clean_data['type'] == 'LIMIT':
            response = order_manager.place_limit_order(
                clean_data['symbol'], clean_data['side'], clean_data['quantity'], clean_data['price']
            )
        elif clean_data['type'] == 'STOP_LIMIT':
            response = order_manager.place_stop_limit_order(
                clean_data['symbol'], clean_data['side'], clean_data['quantity'], clean_data['price'], clean_data['stop_price']
            )
            
        return {
            "success": True,
            "message": "Order placed successfully!",
            "details": OrderManager.format_order_response(response)
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error("API Error: %s", str(e))
        raise HTTPException(status_code=502, detail=f"API Error: {str(e)}")

@app.get("/account")
async def get_account():
    try:
        client_wrapper = BinanceClient()
        account_info = client_wrapper.connect() # connect() calls /fapi/v2/account
        
        # Simplify balance for UI
        balances = account_info.get("assets", [])
        usdt_balance = next((b for b in balances if b["asset"] == "USDT"), {"walletBalance": "0.00"})
        
        return {
            "success": True,
            "wallet_balance": usdt_balance.get("walletBalance", "0.00"),
            "assets_count": len(balances)
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"API Error: {str(e)}")

@app.get("/price/{symbol}")
async def get_price(symbol: str):
    try:
        client_wrapper = BinanceClient()
        endpoint = "/fapi/v1/ticker/price"
        params = {"symbol": symbol.upper()}
        response = client_wrapper.request("GET", endpoint, params=params)
        return response
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"API Error: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "healthy"}
