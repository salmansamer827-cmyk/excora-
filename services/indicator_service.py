import requests
import numpy as np

BINANCE_URL = "https://api.binance.com/api/v3"


# =========================
# 📈 Get Candles Data
# =========================
def get_candles(symbol="BTCUSDT", interval="1h", limit=200):
    try:
        url = f"{BINANCE_URL}/klines?symbol={symbol.upper()}&interval={interval}&limit={limit}"
        res = requests.get(url, timeout=5)
        data = res.json()

        closes = [float(c[4]) for c in data]
        return np.array(closes)

    except Exception as e:
        return []


# =========================
# 📊 Moving Average (SMA)
# =========================
def sma(data, period=14):
    if len(data) < period:
        return []

    result = []

    for i in range(len(data)):
        if i < period:
            result.append(None)
        else:
            avg = np.mean(data[i - period:i])
            result.append(float(avg))

    return result


# =========================
# 📉 RSI (Relative Strength Index)
# =========================
def rsi(data, period=14):
    if len(data) < period + 1:
        return []

    deltas = np.diff(data)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.zeros_like(data)
    avg_loss = np.zeros_like(data)

    avg_gain[period] = np.mean(gains[:period])
    avg_loss[period] = np.mean(losses[:period])

    for i in range(period + 1, len(data)):
        avg_gain[i] = (avg_gain[i - 1] * (period - 1) + gains[i - 1]) / period
        avg_loss[i] = (avg_loss[i - 1] * (period - 1) + losses[i - 1]) / period

    rs = np.divide(avg_gain, avg_loss, out=np.zeros_like(avg_gain), where=avg_loss != 0)
    rsi = 100 - (100 / (1 + rs))

    return rsi.tolist()


# =========================
# 📊 MACD Indicator
# =========================
def ema(data, period):
    alpha = 2 / (period + 1)
    ema_values = []

    for i, price in enumerate(data):
        if i == 0:
            ema_values.append(price)
        else:
            ema_values.append((price * alpha) + (ema_values[i - 1] * (1 - alpha)))

    return np.array(ema_values)


def macd(data):
    if len(data) < 26:
        return []

    ema12 = ema(data, 12)
    ema26 = ema(data, 26)

    macd_line = ema12 - ema26
    signal_line = ema(macd_line, 9)
    histogram = macd_line - signal_line

    return {
        "macd": macd_line.tolist(),
        "signal": signal_line.tolist(),
        "histogram": histogram.tolist()
    }


# =========================
# 🚀 Full Indicators Bundle
# =========================
def get_indicators(symbol="BTCUSDT", interval="1h"):
    closes = get_candles(symbol, interval)

    if len(closes) == 0:
        return {"error": "no data"}

    return {
        "symbol": symbol,
        "interval": interval,
        "sma_14": sma(closes, 14),
        "rsi_14": rsi(closes, 14),
        "macd": macd(closes)
    }