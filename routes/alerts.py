from flask import Blueprint, jsonify, request
import requests
import time

alerts_bp = Blueprint("alerts", __name__)

BINANCE_URL = "https://api.binance.com/api/v3"


# =========================
# 🧠 TEMP MEMORY (MVP)
# =========================
alerts = []


# =========================
# ➕ Create Alert
# =========================
@alerts_bp.route("/create", methods=["POST"])
def create_alert():
    data = request.json

    symbol = data.get("symbol", "").upper()
    target_price = float(data.get("target_price", 0))

    if not symbol or target_price <= 0:
        return jsonify({"error": "invalid data"}), 400

    alert = {
        "id": len(alerts) + 1,
        "symbol": symbol,
        "target_price": target_price,
        "created_at": int(time.time()),
        "triggered": False
    }

    alerts.append(alert)

    return jsonify({
        "message": "alert created",
        "alert": alert
    })


# =========================
# 📋 Get All Alerts
# =========================
@alerts_bp.route("/list", methods=["GET"])
def list_alerts():
    return jsonify(alerts)


# =========================
# 🔍 Check Alerts (manual trigger check)
# =========================
@alerts_bp.route("/check", methods=["GET"])
def check_alerts():
    triggered = []

    for alert in alerts:
        if alert["triggered"]:
            continue

        try:
            url = f"{BINANCE_URL}/ticker/price?symbol={alert['symbol']}"
            res = requests.get(url, timeout=5)
            data = res.json()

            current_price = float(data.get("price", 0))

            if current_price >= alert["target_price"]:
                alert["triggered"] = True
                alert["triggered_price"] = current_price
                alert["triggered_at"] = int(time.time())

                triggered.append(alert)

        except Exception as e:
            continue

    return jsonify({
        "message": "alerts checked",
        "triggered": triggered
    })


# =========================
# ❌ Delete Alert
# =========================
@alerts_bp.route("/delete/<int:alert_id>", methods=["DELETE"])
def delete_alert(alert_id):
    global alerts

    alerts = [a for a in alerts if a["id"] != alert_id]

    return jsonify({
        "message": "alert deleted",
        "alerts": alerts
    })