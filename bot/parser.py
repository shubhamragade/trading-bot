import re
import logging
from typing import Optional, Dict, Any

class CommandParser:
    """
    Parses natural language strings into structured trading commands.
    Demonstrates intent extraction without requiring an external NLP API.
    """
    
    @staticmethod
    def parse(text: str) -> Optional[Dict[str, Any]]:
        text = text.lower().strip()
        
        # Mapping long/short to buy/sell
        text = text.replace("long", "buy").replace("short", "sell")
        
        # Regex Patterns
        # 1. MARKET: "buy 0.01 btc" or "market sell 0.5 eth"
        market_pattern = r"(market\s+)?(buy|sell)\s+([\d.]+)\s+([a-z0-9]+)(\s+at\s+market)?"
        
        # 2. LIMIT: "buy 0.01 btc at 45000" or "limit sell 0.5 eth at 2500"
        limit_pattern = r"(limit\s+)?(buy|sell)\s+([\d.]+)\s+([a-z0-9]+)\s+at\s+([\d.]+)"
        
        # 3. STOP_LIMIT: "stop limit buy 0.01 btc price 45000 trigger 44000"
        stop_limit_pattern = r"stop\s+limit\s+(buy|sell)\s+([\d.]+)\s+([a-z0-9]+)\s+price\s+([\d.]+)\s+trigger\s+([\d.]+)"

        # Try STOP_LIMIT first (strictest pattern)
        match = re.search(stop_limit_pattern, text)
        if match:
            side, qty, symbol, price, stop = match.groups()
            return {
                "type": "STOP_LIMIT",
                "side": side.upper(),
                "quantity": float(qty),
                "symbol": CommandParser._format_symbol(symbol),
                "price": float(price),
                "stop_price": float(stop)
            }

        # Try LIMIT
        match = re.search(limit_pattern, text)
        if match:
            _, side, qty, symbol, price = match.groups()
            return {
                "type": "LIMIT",
                "side": side.upper(),
                "quantity": float(qty),
                "symbol": CommandParser._format_symbol(symbol),
                "price": float(price)
            }

        # Try MARKET
        match = re.search(market_pattern, text)
        if match:
            _, side, qty, symbol, _ = match.groups()
            return {
                "type": "MARKET",
                "side": side.upper(),
                "quantity": float(qty),
                "symbol": CommandParser._format_symbol(symbol)
            }

        return None

    @staticmethod
    def _format_symbol(symbol: str) -> str:
        symbol = symbol.upper()
        if not symbol.endswith("USDT") and symbol in ["BTC", "ETH", "BNB", "SOL"]:
            return f"{symbol}USDT"
        return symbol

if __name__ == "__main__":
    # Quick Test
    test_cases = [
        "buy 0.01 btc at market",
        "limit sell 0.5 eth at 2500",
        "stop limit buy 0.002 btc price 100000 trigger 99000",
        "Buy 0.1 SOL at 120"
    ]
    for tc in test_cases:
        print(f"Input: {tc} -> Output: {CommandParser.parse(tc)}")
