from flask import Blueprint, request, jsonify
from db import get_connection
from utils.jwt_util import decode_token

events_bp = Blueprint("events", __name__)

def get_user_from_request(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    token = auth_header.split(" ")[1]
    return decode_token(token)


@events_bp.route("/events", methods=["GET"])
def get_events():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events ORDER BY datetime ASC")
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(events)


@events_bp.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    event = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(event)


@events_bp.route("/events", methods=["POST"])
def create_event():
    user = get_user_from_request(request)
    print(user)
    if not user or user['role'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 403

    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (name, description, datetime, location) VALUES (%s, %s, %s, %s)",
                   (data["name"], data["description"], data["datetime"], data["location"]))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Event created"}), 201


@events_bp.route("/events/<int:event_id>/rsvp", methods=["POST"])
def rsvp_event(event_id):
    user = get_user_from_request(request)
    if not user:
        return jsonify({"message": "Unauthorized"}), 403

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO rsvps (user_id, event_id) VALUES (%s, %s)", (user["user_id"], event_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "RSVP added"})


@events_bp.route("/events/<int:event_id>/rsvps", methods=["GET"])
def get_event_rsvps(event_id):
    # user = get_user_from_request(request)
    # if not user or user['role'] != 'admin':
    #     return jsonify({"message": "Unauthorized"}), 403

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT users.id as user_id, users.name FROM rsvps JOIN users ON rsvps.user_id = users.id WHERE rsvps.event_id = %s", (event_id,))
    rsvps = [{"user_id": row[0], "name": row[1]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(rsvps)