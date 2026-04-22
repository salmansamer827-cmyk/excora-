import requests
from ..config import Config

class BinanceService:
    @staticmethod
    def get_price(symbol: str):
        try:
            url = f"{Config.BINANCE_API_URL}/ticker/price?symbol={symbol.upper()}"
            response = requests.get(url)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
