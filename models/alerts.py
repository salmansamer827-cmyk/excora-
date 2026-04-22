from flask import Blueprint, jsonify, request
import time

alerts_bp = Blueprint("alerts", __name__)

# =========================
# 🧠 TEMP STORAGE (MVP ONLY)
# =========================
# شكل البيانات:
# {
#   "user1": [
#       {"symbol": "BTCUSDT", "target": 70000, "active": True}
#   ]
# }
alerts_store = {}


# =========================
# ➕ Create Alert
# =========================
@alerts_bp.route("/create", methods=["POST"])
def create_alert():
    data = request.json

    username = data.get("username")
    symbol = data.get("symbol", "").upper()
    target = float(data.get("target_price", 0))

    if not username or not symbol or target <= 0:
        return jsonify({"error": "invalid data"}), 400

    if username not in alerts_store:
        alerts_store[username] = []

    alert = {
        "id": len(alerts_store[username]) + 1,
        "symbol": symbol,
        "target_price": target,
        "created_at": int(time.time()),
        "triggered": False
    }

    alerts_store[username].append(alert)

    return jsonify({
        "message": "alert created",
        "alert": alert
    })


# =========================
# 📋 Get User Alerts
# =========================
@alerts_bp.route("/<username>", methods=["GET"])
def get_alerts(username):
    return jsonify({
        "username": username,
        "alerts": alerts_store.get(username, [])
    })


# =========================
# 🔍 Check Alerts (Manual Trigger)
# =========================
@alerts_bp.route("/check/<username>", methods=["GET"])
def check_alerts(username):
    from services.binance_service import get_price

    if username not in alerts_store:
        return jsonify({"alerts": []})

    triggered = []

    for alert in alerts_store[username]:
        if alert["triggered"]:
            continue

        price_data = get_price(alert["symbol"])
        current_price = float(price_data.get("price", 0))

        if current_price >= alert["target_price"]:
            alert["triggered"] = True
            alert["triggered_at"] = int(time.time())
            alert["current_price"] = current_price

            triggered.append(alert)

    return jsonify({
        "username": username,
        "triggered": triggered
    })


# =========================
# ❌ Delete Alert
# =========================
@alerts_bp.route("/delete", methods=["POST"])
def delete_alert():
    data = request.json

    username = data.get("username")
    alert_id = data.get("alert_id")

    if username not in alerts_store:
        return jsonify({"error": "user not found"}), 404

    alerts_store[username] = [
        a for a in alerts_store[username] if a["id"] != alert_id
    ]

    return jsonify({
        "message": "alert deleted",
        "alerts": alerts_store[username]
    })