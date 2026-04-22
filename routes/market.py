from fastapi import APIRouter
from ..services.binance_service import BinanceService

router = APIRouter(prefix="/market", tags=["Market Analysis"])

@router.get("/price/{symbol}")
def get_crypto_price(symbol: str):
    return BinanceService.get_price(symbol)
