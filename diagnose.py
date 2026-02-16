import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

load_dotenv()

def diagnose():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    print(f"Testing with API Key: {api_key[:5]}...{api_key[-5:]}")
    
    # Try multiple ways to initialize
    configs = [
        {"name": "testnet=True (Standard)", "params": {"testnet": True}},
        {"name": "Explicit Futures Testnet URL", "params": {"testnet": True}, "url": "https://testnet.binancefuture.com/fapi"}
    ]
    
    for config in configs:
        print(f"\n--- Testing Configuration: {config['name']} ---")
        try:
            client = Client(api_key, api_secret, **config['params'])
            if "url" in config:
                client.FUTURES_URL = config['url']
                client.API_URL = "https://testnet.binancefuture.com"
                
            # Try getting spot account first
            try:
                spot_account = client.get_account()
                print("✅ SUCCESS: Found Spot Account! (Keys might be for Spot Testnet)")
            except Exception:
                print("❌ Spot Account check failed.")

            # Try getting futures account
            account = client.futures_account()
            print("✅ SUCCESS: Found Futures Account!")
            return True
        except BinanceAPIException as e:
            print(f"❌ API Error: {e.code} - {e.message}")
        except Exception as e:
            print(f"❌ Unexpected Error: {type(e).__name__} - {str(e)}")
            
    return False

if __name__ == "__main__":
    diagnose()
