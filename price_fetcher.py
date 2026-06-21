import requests
import os
import time
from signal_analyzer import analyze_engulfing_signal
from bot import send_signal_to_discord

TWELVE_KEY = os.getenv("TWELVE_DATA_KEY")

PAIR_SYMBOLS = {
    "USDJPY": "USD/JPY",
    "GBPUSD": "GBP/USD",
    "GBPJPY": "GBP/JPY",
}

def get_candles(symbol: str):
    """ดึงแท่งเทียน 15 นาทีจาก Twelve Data"""
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol":     symbol,
        "interval":   "15min",
        "outputsize": 5,
        "apikey":     TWELVE_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") == "error":
        print(f"❌ API Error for {symbol}: {data.get('message')}")
        return None

    candles = []
    for bar in data.get("values", []):
        candles.append({
            "open":  float(bar["open"]),
            "high":  float(bar["high"]),
            "low":   float(bar["low"]),
            "close": float(bar["close"]),
        })
    return candles  # index 0 = แท่งล่าสุด

def check_engulfing(candles):
    if not candles or len(candles) < 2:
        return None

    curr = candles[0]
    prev = candles[1]

    curr_body = curr["close"] - curr["open"]
    prev_body = prev["close"] - prev["open"]

    if (prev_body < 0 and curr_body > 0 and
        curr["open"] < prev["close"] and
        curr["close"] > prev["open"]):
        return "bullish_engulfing"

    if (prev_body > 0 and curr_body < 0 and
        curr["open"] > prev["close"] and
        curr["close"] < prev["open"]):
        return "bearish_engulfing"

    return None

def run_check():
    print("🔍 Checking pairs...")

    for pair, symbol in PAIR_SYMBOLS.items():
        try:
            candles = get_candles(symbol)
            if not candles:
                print(f"⚠️ {pair}: Could not fetch data")
                continue

            candle_type = check_engulfing(candles)

            if candle_type:
                curr = candles[0]
                prev = candles[1]
                data = {
                    "pair":       pair,
                    "candle_type": candle_type,
                    "close":      curr["close"],
                    "open":       curr["open"],
                    "high":       curr["high"],
                    "low":        curr["low"],
                    "prev_close": prev["close"],
                    "prev_open":  prev["open"],
                }
                analysis = analyze_engulfing_signal(data)
                if analysis["valid"]:
                    send_signal_to_discord(analysis)
                    print(f"✅ Signal sent: {pair} {candle_type}")
                else:
                    print(f"⚠️ {pair}: Engulfing found but no S/R confluence")
            else:
                print(f"➖ {pair}: No signal")

            time.sleep(1)  # หน่วง 1 วิ ป้องกัน rate limit

        except Exception as e:
            print(f"❌ Error {pair}: {e}")

if __name__ == "__main__":
    run_check()