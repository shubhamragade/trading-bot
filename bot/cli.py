import argparse
import logging
import sys
import questionary
from bot.logging_config import setup_logging
from bot.client import BinanceClient
from bot.orders import OrderManager
from bot.validators import InputValidator
from binance.exceptions import BinanceAPIException, BinanceOrderException

def print_summary(data: dict):
    print("\n===== ORDER REQUEST =====")
    print(f"Symbol: {data['symbol']}")
    print(f"Side: {data['side']}")
    print(f"Type: {data['type']}")
    print(f"Quantity: {data['quantity']}")
    if data.get('price'):
        print(f"Price: {data['price']}")
    if data.get('stop_price'):
        print(f"Trigger: {data['stop_price']}")
    print("-" * 25)

def interactive_mode():
    """
    Runs the bot in a professional interactive mode.
    """
    print("\n--- Binance Futures Trading Bot (Interactive) ---")
    
    symbol = questionary.text("Enter symbol (e.g., BTCUSDT):", default="BTCUSDT").ask()
    side = questionary.select("BUY or SELL:", choices=["BUY", "SELL"]).ask()
    order_type = questionary.select("Order Type:", choices=["MARKET", "LIMIT", "STOP_LIMIT"]).ask()
    quantity = questionary.text("Quantity:").ask()
    
    price = None
    if order_type in ["LIMIT", "STOP_LIMIT"]:
        price = questionary.text("Price:").ask()
        
    stop_price = None
    if order_type == "STOP_LIMIT":
        stop_price = questionary.text("Trigger Price (Stop Price):").ask()
        
    # Confirm
    confirm = questionary.confirm("Confirm order placement?", default=False).ask()
    if not confirm:
        print("❌ Order cancelled.")
        return None

    return {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "price": price,
        "stop_price": stop_price
    }

def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", choices=["MARKET", "LIMIT", "STOP_LIMIT"], help="Order type")
    parser.add_argument("--quantity", type=str, help="Order quantity")
    parser.add_argument("--price", type=str, help="Limit price")
    parser.add_argument("--stop", type=str, help="Stop price (for STOP_LIMIT)")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    order_data = None
    
    if args.interactive:
        order_data = interactive_mode()
        if not order_data:
            return
    elif args.symbol and args.side and args.type and args.quantity:
        order_data = {
            "symbol": args.symbol,
            "side": args.side,
            "type": args.type,
            "quantity": args.quantity,
            "price": args.price,
            "stop_price": args.stop
        }
    else:
        parser.print_help()
        print("\nNote: Use --interactive for a guided experience.")
        sys.exit(0)

    # 1. Validate
    try:
        clean_data = InputValidator.validate_inputs(
            order_data['symbol'], 
            order_data['side'], 
            order_data['type'], 
            order_data['quantity'],
            order_data.get('price'),
            order_data.get('stop_price')
        )
    except ValueError as e:
        print(str(e))
        logging.error("Validation failed: %s", str(e))
        return

    # 2. Print Request Summary
    print_summary(clean_data)

    # 3. Connect & Place Order
    try:
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
            
        # 4. Show Response
        print(OrderManager.format_order_response(response))
        print("\n✅ SUCCESS")
        logging.info("Response received: %s", response.get('status'))
        
    except BinanceAPIException as e:
        print(f"\n❌ API ERROR: {e.message}")
        logging.error("API Error: %s", e.message)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        logging.error("Unexpected Error: %s", str(e))

if __name__ == "__main__":
    main()
