from flask import Flask, request, jsonify
from signal_analyzer import analyze_engulfing_signal
from bot import send_signal_to_discord
from config import TRADINGVIEW_SECRET
import hmac, hashlib

app = Flask(__name__)

def verify_secret(req_secret: str) -> bool:
    return hmac.compare_digest(req_secret or "", TRADINGVIEW_SECRET or "")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    # ตรวจสอบ secret
    if not verify_secret(data.get("secret")):
        return jsonify({"error": "Unauthorized"}), 401

    # วิเคราะห์สัญญาณ
    analysis = analyze_engulfing_signal(data)

    if analysis["valid"]:
        status = send_signal_to_discord(analysis)
        return jsonify({"status": "Signal sent", "discord_status": status}), 200
    else:
        return jsonify({"status": "No valid signal", "reason": analysis.get("reason")}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)