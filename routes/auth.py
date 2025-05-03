from flask import Blueprint, request, jsonify
from db import get_connection
from utils.jwt_util import generate_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, 'user')",
                   (data["name"], data["email"], data["password"]))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User created"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, role FROM users WHERE email=%s AND password=%s",
                   (data["email"], data["password"]))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    token = generate_token(user["id"], user["role"])
    return jsonify({"token": token, "role": user["role"]})