import logging

class InputValidator:
    """
    Validates user input before sending it to the Binance API.
    """
    
    @staticmethod
    def validate_symbol(symbol: str):
        """
        Validates the trading symbol (e.g., BTCUSDT).
        """
        if not symbol or not isinstance(symbol, str):
            raise ValueError("❌ Symbol must be a non-empty string (e.g., BTCUSDT)")
        
        # Simple check for USDT-M futures pairs
        if not symbol.endswith("USDT") and not symbol.endswith("BUSD"):
             logging.warning("Symbol %s might not be a valid USDT-M or BUSD-M futures pair.", symbol)
        
        return symbol.upper()

    @staticmethod
    def validate_side(side: str):
        """
        Validates the order side (BUY or SELL).
        """
        side = side.upper()
        if side not in ["BUY", "SELL"]:
            raise ValueError("❌ Side must be either BUY or SELL")
        return side

    @staticmethod
    def validate_order_type(order_type: str):
        """
        Validates the order type.
        """
        order_type = order_type.upper()
        valid_types = ["MARKET", "LIMIT", "STOP_LIMIT"]
        if order_type not in valid_types:
            raise ValueError(f"❌ Order type must be one of {', '.join(valid_types)}")
        return order_type

    @staticmethod
    def validate_quantity(quantity: float):
        """
        Validates that the quantity is a positive number.
        """
        try:
            qty = float(quantity)
            if qty <= 0:
                raise ValueError("❌ Quantity must be positive")
            return qty
        except (TypeError, ValueError):
            raise ValueError("❌ Quantity must be a valid number and greater than 0")

    @staticmethod
    def validate_price(price: float, optional: bool = False):
        """
        Validates that the price is a positive number.
        """
        if optional and price is None:
            return None
        
        try:
            p = float(price)
            if p <= 0:
                raise ValueError("❌ Price must be positive")
            return p
        except (TypeError, ValueError):
            raise ValueError("❌ Price must be a valid number and greater than 0")

    @staticmethod
    def validate_inputs(symbol, side, order_type, quantity, price=None, stop_price=None):
        """
        Comprehensive validation of all order parameters.
        """
        clean_symbol = InputValidator.validate_symbol(symbol)
        clean_side = InputValidator.validate_side(side)
        clean_type = InputValidator.validate_order_type(order_type)
        clean_qty = InputValidator.validate_quantity(quantity)
        
        clean_price = None
        if clean_type in ["LIMIT", "STOP_LIMIT"]:
            clean_price = InputValidator.validate_price(price)
        
        clean_stop = None
        if clean_type == "STOP_LIMIT":
            clean_stop = InputValidator.validate_price(stop_price)
            
        return {
            "symbol": clean_symbol,
            "side": clean_side,
            "type": clean_type,
            "quantity": clean_qty,
            "price": clean_price,
            "stop_price": clean_stop
        }
