import asyncio
import json
import websockets
from threading import Thread

# =========================
# 📡 WebSocket Stream URL (Binance)
# =========================
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws"


# =========================
# 🧠 Global Subscribers
# (Frontend connections will be stored here later)
# =========================
subscribers = set()


# =========================
# 📊 Subscribe Client (React / Frontend)
# =========================
def add_subscriber(ws):
    subscribers.add(ws)


def remove_subscriber(ws):
    subscribers.discard(ws)


# =========================
# 🔥 Broadcast Data to All Clients
# =========================
async def broadcast(data):
    if not subscribers:
        return

    message = json.dumps(data)

    dead_clients = []

    for ws in subscribers:
        try:
            await ws.send(message)
        except:
            dead_clients.append(ws)

    for dc in dead_clients:
        subscribers.discard(dc)


# =========================
# 📈 Binance Live Stream Handler
# =========================
async def binance_stream(symbol="btcusdt"):
    stream_url = f"{BINANCE_WS_URL}/{symbol.lower()}@trade"

    async with websockets.connect(stream_url) as websocket:
        print(f"🔥 Connected to Binance stream: {symbol}")

        while True:
            try:
                data = await websocket.recv()
                trade = json.loads(data)

                formatted_data = {
                    "symbol": trade["s"],
                    "price": float(trade["p"]),
                    "quantity": float(trade["q"]),
                    "time": trade["T"]
                }

                await broadcast(formatted_data)

            except Exception as e:
                print("WebSocket error:", e)
                break


# =========================
# 🚀 Run WebSocket in Background Thread
# =========================
def start_websocket(symbol="btcusdt"):
    loop = asyncio.new_event_loop()

    def runner():
        asyncio.set_event_loop(loop)
        loop.run_until_complete(binance_stream(symbol))

    thread = Thread(target=runner)
    thread.daemon = True
    thread.start()

    print("🚀 WebSocket service started")