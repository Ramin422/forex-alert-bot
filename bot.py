import requests
import json
from datetime import datetime
from config import DISCORD_WEBHOOK_URL

SIGNAL_EMOJI = {"BUY": "🟢", "SELL": "🔴"}
STRENGTH_LABEL = {
    range(0, 3):  ("⭐", "Weak"),
    range(3, 6):  ("⭐⭐", "Moderate"),
    range(6, 100): ("⭐⭐⭐", "Strong"),
}

def get_strength_label(score: int):
    for r, label in STRENGTH_LABEL.items():
        if score in r:
            return label
    return ("⭐", "Weak")

def send_signal_to_discord(analysis: dict):
    """ส่ง embed message แจ้งเตือนสัญญาณเทรดไปยัง Discord"""
    if not analysis.get("valid"):
        return

    signal = analysis["signal"]
    pair = analysis["pair"]
    price = analysis["price"]
    stars, label = get_strength_label(analysis["strength"])
    confluence_text = "\n".join(analysis["confluence"])
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    color = 0x00FF00 if signal == "BUY" else 0xFF0000

    embed = {
        "embeds": [{
            "title": f"{SIGNAL_EMOJI[signal]} {signal} Signal — {pair}",
            "color": color,
            "fields": [
                {"name": "💹 Entry Price",  "value": f"`{price}`",                          "inline": True},
                {"name": "🛑 Stop Loss",    "value": f"`{analysis['sl']}`",                 "inline": True},
                {"name": "🎯 TP1 / TP2",   "value": f"`{analysis['tp1']}` / `{analysis['tp2']}`", "inline": True},
                {"name": "📊 R:R Ratio",   "value": f"`1 : {analysis['rr_ratio']}`",        "inline": True},
                {"name": "🕯️ Pattern",     "value": f"`{analysis['candle_type'].replace('_', ' ').title()}`", "inline": True},
                {"name": "💪 Strength",    "value": f"{stars} {label}",                     "inline": True},
                {"name": "🏗️ Confluence",  "value": confluence_text or "None",              "inline": False},
            ],
            "footer": {"text": f"Forex Signal Bot • {now}"},
            "thumbnail": {"url": "https://i.imgur.com/forex_icon.png"},
        }]
    }

    response = requests.post(
        DISCORD_WEBHOOK_URL,
        data=json.dumps(embed),
        headers={"Content-Type": "application/json"}
    )
    return response.status_code