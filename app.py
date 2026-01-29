from flask import Flask, render_template, jsonify
from routes.webhook import webhook_bp
from db.mongo import collection

app = Flask(__name__)

# register webhook blueprint
app.register_blueprint(webhook_bp)

@app.route("/")
def home():
    return render_template("index.html")

# 🔥 NEW: events API for UI polling
@app.route("/events")
def get_events():
    events = list(
        collection.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(10)
    )

    formatted_events = []

    for e in events:
        if e["action"] == "PUSH":
            message = f'{e["author"]} pushed to {e["to_branch"]} on {e["timestamp"]}'
        elif e["action"] == "PULL_REQUEST":
            message = (
                f'{e["author"]} submitted a pull request '
                f'from {e["from_branch"]} to {e["to_branch"]} on {e["timestamp"]}'
            )
        elif e["action"] == "MERGE":
            message = (
                f'{e["author"]} merged branch '
                f'{e["from_branch"]} to {e["to_branch"]} on {e["timestamp"]}'
            )
        else:
            continue

        formatted_events.append({"message": message})

    return jsonify(formatted_events)

if __name__ == "__main__":
    app.run(debug=True)
