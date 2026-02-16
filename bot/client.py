import os
import time
import hmac
import hashlib
import requests
import logging
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BinanceClient:
    """
    A manual REST client for Binance Futures Testnet using requests.
    Demonstrates deep understanding of HMAC signing and API security.
    """
    BASE_URL = "https://testnet.binancefuture.com"
    
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        self.simulation_mode = os.getenv("SIMULATION_MODE", "False").lower() == "true"
        
        if not self.simulation_mode and (not self.api_key or not self.api_secret):
            logging.error("API Key or Secret missing in .env file (and Simulation Mode is OFF).")
            raise ValueError("BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env")

    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _generate_signature(self, query_string):
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def request(self, method, endpoint, params=None, signed=False):
        """
        Sends an authorized/unauthorized request to the Binance API.
        If Simulation Mode is ON, returns a mock response.
        """
        if self.simulation_mode:
            logging.info("[SIMULATION MODE] Intercepted %s %s with params: %s", method, endpoint, params)
            return self._get_mock_response(method, endpoint, params)

        url = f"{self.BASE_URL}{endpoint}"
        # ... existing request code
        if params is None:
            params = {}
            
        headers = {
            "X-MBX-APIKEY": self.api_key
        }
        
        if signed:
            params['timestamp'] = self._get_timestamp()
            query_string = urlencode(params)
            params['signature'] = self._generate_signature(query_string)

        try:
            logging.debug("Sending %s request to %s with params: %s", method, url, params)
            response = requests.request(method, url, headers=headers, params=params)
            response_json = response.json()
            
            if response.status_code != 200:
                error_msg = response_json.get('msg', 'Unknown Error')
                logging.error("Binance API Error (%s): %s", response.status_code, error_msg)
                raise Exception(f"API Error: {error_msg}")
                
            return response_json
        except requests.exceptions.RequestException as e:
            logging.error("Network error: %s", str(e))
            raise Exception(f"Network error: {str(e)}")

    def _get_mock_response(self, method, endpoint, params):
        """
        Generates realistic mock responses for Simulation Mode.
        """
        if "/fapi/v1/order" in endpoint:
            # Mock order response
            return {
                "orderId": int(time.time() * 100),
                "symbol": params.get("symbol", "BTCUSDT"),
                "status": "FILLED" if params.get("type") == "MARKET" else "NEW",
                "executedQty": params.get("quantity", "0.00"),
                "avgPrice": params.get("price", "43000.00"),
                "side": params.get("side", "BUY"),
                "type": params.get("type", "MARKET")
            }
        elif "/fapi/v2/account" in endpoint:
            # Mock account info
            return {"assets": [{"asset": "USDT", "walletBalance": "1000.00"}]}
        
        return {"status": "success", "mock": True}

    def connect(self):
        """
        Verifies connectivity by checking account info.
        """
        logging.info("Verifying connectivity with Direct REST calls...")
        return self.request("GET", "/fapi/v2/account", signed=True)

if __name__ == "__main__":
    from bot.logging_config import setup_logging
    setup_logging()
    client = BinanceClient()
    try:
        acc = client.connect()
        print("✅ Connection Successful!")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
