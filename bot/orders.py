import logging
from bot.client import BinanceClient

class OrderManager:
    """
    Handles order placement logic using direct REST calls through BinanceClient.
    """
    def __init__(self, client: BinanceClient):
        self.client = client

    def place_market_order(self, symbol: str, side: str, quantity: float):
        """
        Places a MARKET order on Binance Futures Testnet.
        """
        logging.info("Placing MARKET %s order for %s, qty: %s", side, symbol, quantity)
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity
        }
        
        response = self.client.request("POST", "/fapi/v1/order", params=params, signed=True)
        logging.info("MARKET order placed successfully. OrderID: %s", response.get('orderId'))
        return response

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float):
        """
        Places a LIMIT order on Binance Futures Testnet.
        """
        logging.info("Placing LIMIT %s order for %s, qty: %s, price: %s", side, symbol, quantity, price)
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "quantity": quantity,
            "price": price,
            "timeInForce": "GTC"  # Good Till Cancelled
        }
        
        response = self.client.request("POST", "/fapi/v1/order", params=params, signed=True)
        logging.info("LIMIT order placed successfully. OrderID: %s", response.get('orderId'))
        return response

    def place_stop_limit_order(self, symbol: str, side: str, quantity: float, price: float, stop_price: float):
        """
        Places a STOP_LIMIT order on Binance Futures Testnet.
        """
        logging.info("Placing STOP_LIMIT %s order for %s, qty: %s, price: %s, stopPrice: %s", 
                    side, symbol, quantity, price, stop_price)
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": "STOP",  # Binance Futures use STOP for stop-limit orders
            "quantity": quantity,
            "price": price,
            "stopPrice": stop_price,
            "timeInForce": "GTC"
        }
        
        response = self.client.request("POST", "/fapi/v1/order", params=params, signed=True)
        logging.info("STOP_LIMIT order placed successfully. OrderID: %s", response.get('orderId'))
        return response

    @staticmethod
    def format_order_response(response: dict):
        """
        Formats the Binance API response for clear CLI output.
        """
        if not response:
            return "No response from Binance."
            
        summary = (
            f"OrderId: {response.get('orderId')}\n"
            f"Status: {response.get('status')}\n"
            f"ExecutedQty: {response.get('executedQty')}\n"
            f"AvgPrice: {response.get('avgPrice', '0.00')}"
        )
        return summary
