from flask import Blueprint, jsonify, request
import hashlib
import time

user_bp = Blueprint("user", __name__)

# =========================
# 🧠 TEMP STORAGE (MVP ONLY)
# ⚠️ لاحقًا يتم استبداله بـ Database
# =========================
users = {}


# =========================
# 🔐 Hash Password
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# =========================
# 🆕 Register
# =========================
@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    if username in users:
        return jsonify({"error": "user already exists"}), 400

    users[username] = {
        "username": username,
        "password": hash_password(password),
        "created_at": int(time.time()),
        "watchlist": []
    }

    return jsonify({
        "message": "user created successfully",
        "username": username
    })


# =========================
# 🔓 Login
# =========================
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    user = users.get(username)

    if not user:
        return jsonify({"error": "user not found"}), 404

    if user["password"] != hash_password(password):
        return jsonify({"error": "wrong password"}), 401

    return jsonify({
        "message": "login successful",
        "username": username,
        "timestamp": int(time.time())
    })


# =========================
# ⭐ Get Watchlist
# =========================
@user_bp.route("/watchlist/<username>", methods=["GET"])
def get_watchlist(username):
    user = users.get(username)

    if not user:
        return jsonify({"error": "user not found"}), 404

    return jsonify(user["watchlist"])


# =========================
# ➕ Add Symbol
# =========================
@user_bp.route("/watchlist/add", methods=["POST"])
def add_watchlist():
    data = request.json

    username = data.get("username")
    symbol = data.get("symbol", "").upper()

    user = users.get(username)

    if not user:
        return jsonify({"error": "user not found"}), 404

    if symbol and symbol not in user["watchlist"]:
        user["watchlist"].append(symbol)

    return jsonify({
        "message": "added",
        "watchlist": user["watchlist"]
    })


# =========================
# ❌ Remove Symbol
# =========================
@user_bp.route("/watchlist/remove", methods=["POST"])
def remove_watchlist():
    data = request.json

    username = data.get("username")
    symbol = data.get("symbol", "").upper()

    user = users.get(username)

    if not user:
        return jsonify({"error": "user not found"}), 404

    if symbol in user["watchlist"]:
        user["watchlist"].remove(symbol)

    return jsonify({
        "message": "removed",
        "watchlist": user["watchlist"]
    })


# =========================
# 👤 Get User Info
# =========================
@user_bp.route("/profile/<username>", methods=["GET"])
def profile(username):
    user = users.get(username)

    if not user:
        return jsonify({"error": "user not found"}), 404

    return jsonify({
        "username": user["username"],
        "created_at": user["created_at"],
        "watchlist_count": len(user["watchlist"])
    })