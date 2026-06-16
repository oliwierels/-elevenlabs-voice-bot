import os
import requests
from flask import Flask, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="static")

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
ELEVENLABS_AGENT_ID = os.environ.get("ELEVENLABS_AGENT_ID")


@app.route("/api/signed-url")
def get_signed_url():
    if not ELEVENLABS_API_KEY or not ELEVENLABS_AGENT_ID:
        return jsonify({"error": "Brak konfiguracji serwera (API key / Agent ID)"}), 500

    response = requests.get(
        f"https://api.elevenlabs.io/v1/convai/conversation/get_signed_url?agent_id={ELEVENLABS_AGENT_ID}",
        headers={"xi-api-key": ELEVENLABS_API_KEY},
        timeout=10,
    )

    if not response.ok:
        return jsonify({"error": "Błąd ElevenLabs API", "details": response.text}), response.status_code

    return jsonify(response.json())


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_static(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
