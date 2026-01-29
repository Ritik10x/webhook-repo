from flask import Blueprint, request, jsonify
from db.mongo import collection
from datetime import datetime

webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("/webhook", methods=["POST"])
def github_webhook():
    payload = request.json
    event_type = request.headers.get("X-GitHub-Event")

    if event_type == "push":
        data = {
            "request_id": payload["after"],
            "author": payload["pusher"]["name"],
            "action": "PUSH",
            "from_branch": payload["ref"].split("/")[-1],
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": payload["head_commit"]["timestamp"]
        }

    elif event_type == "pull_request":
        pr = payload["pull_request"]
        data = {
            "request_id": pr["id"],
            "author": pr["user"]["login"],
            "action": "PULL_REQUEST",
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": pr["created_at"]
        }

    else:
        return jsonify({"message": "Event ignored"}), 200

    # Avoid duplicates
    if not collection.find_one({"request_id": data["request_id"]}):
        collection.insert_one(data)

    return jsonify({"status": "stored"}), 200
