from flask import Blueprint, jsonify, request
import time

watchlist_bp = Blueprint("watchlist", __name__)

# =========================
# 🧠 TEMP STORAGE (MVP ONLY)
# =========================
# شكل البيانات:
# {
#   "user1": ["BTCUSDT", "ETHUSDT"]
# }
watchlists = {}


# =========================
# 👤 Get User Watchlist
# =========================
@watchlist_bp.route("/<username>", methods=["GET"])
def get_watchlist(username):
    user_list = watchlists.get(username, [])

    return jsonify({
        "username": username,
        "watchlist": user_list,
        "count": len(user_list)
    })


# =========================
# ➕ Add Symbol
# =========================
@watchlist_bp.route("/add", methods=["POST"])
def add_symbol():
    data = request.json

    username = data.get("username")
    symbol = data.get("symbol", "").upper()

    if not username or not symbol:
        return jsonify({"error": "missing data"}), 400

    if username not in watchlists:
        watchlists[username] = []

    if symbol not in watchlists[username]:
        watchlists[username].append(symbol)

    return jsonify({
        "message": "symbol added",
        "watchlist": watchlists[username]
    })


# =========================
# ❌ Remove Symbol
# =========================
@watchlist_bp.route("/remove", methods=["POST"])
def remove_symbol():
    data = request.json

    username = data.get("username")
    symbol = data.get("symbol", "").upper()

    if username not in watchlists:
        return jsonify({"error": "user not found"}), 404

    if symbol in watchlists[username]:
        watchlists[username].remove(symbol)

    return jsonify({
        "message": "symbol removed",
        "watchlist": watchlists[username]
    })


# =========================
# 🧹 Clear Watchlist
# =========================
@watchlist_bp.route("/clear/<username>", methods=["DELETE"])
def clear_watchlist(username):
    watchlists[username] = []

    return jsonify({
        "message": "watchlist