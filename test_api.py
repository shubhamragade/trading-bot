import requests
import json

def test_api():
    url = "http://127.0.0.1:8000/place_order"
    
    # Test case: Valid-looking MARKET BUY
    payload = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "MARKET",
        "quantity": 0.002
    }
    
    print(f"Testing POST {url} with payload: {payload}")
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
