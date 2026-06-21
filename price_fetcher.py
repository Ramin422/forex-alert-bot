import requests
import os
import sys
from signal_analyzer import analyze_engulfing_signal
from bot import send_signal_to_discord

ALPHA_KEY = os.getenv("ALPHA_VANTAGE_KEY")

PAIR_SYMBOLS = {
    "USDJPY": "USD/JPY",
    "GBPUSD": "GBP/USD",
    "GBPJPY": "GBP/JPY",
}

def get_candles(from_symbol: str, to_symbol: str):
    """ดึงข้อมูลแท่งเทียน 15 นาทีจาก Alpha Vantage"""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "FX_INTRADAY",
        "from_symbol": from_symbol,
        "to_symbol": to_symbol,
        "interval": "15min",
        "outputsize": "compact",
        "apikey": ALPHA_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()

    key = "Time Series FX (15min)"
    if key not in data:
        print(f"❌ API Error for {from_symbol}/{to_symbol}: {data.get('Note') or data.get('Information') or data}")
        return None

    # แปลงเป็น list เรียงตามเวลา (ใหม่ → เก่า)
    candles = []
    for timestamp, values in data[key].items():
        candles.append({
            "time": timestamp,
            "open":  float(values["1. open"]),
            "high":  float(values["2. high"]),
            "low":   float(values["3. low"]),
            "close": float(values["4. close"]),
        })
    return candles  # index 0 = ล่าสุด

def check_engulfing(candles):
    """เช็ค Engulfing จาก 2 แท่งล่าสุด"""
    if not candles or len(candles) < 2:
        return None

    curr = candles[0]   # แท่งล่าสุด
    prev = candles[1]   # แท่งก่อนหน้า

    curr_body = curr["close"] - curr["open"]
    prev_body = prev["close"] - prev["open"]

    # Bullish Engulfing
    if (prev_body < 0 and curr_body > 0 and
        curr["open"] < prev["close"] and
        curr["close"] > prev["open"]):
        return "bullish_engulfing"

    # Bearish Engulfing
    if (prev_body > 0 and curr_body < 0 and
        curr["open"] > prev["close"] and
        curr["close"] < prev["open"]):
        return "bearish_engulfing"

    return None

def run_check():
    print("🔍 Checking pairs...")

    for pair, symbol in PAIR_SYMBOLS.items():
        from_sym, to_sym = symbol.split("/")
        try:
            candles = get_candles(from_sym, to_sym)
            if not candles:
                print(f"⚠️ {pair}: Could not fetch data")
                continue

            candle_type = check_engulfing(candles)
            curr = candles[0]
            prev = candles[1]

            if candle_type:
                data = {
                    "pair": pair,
                    "candle_type": candle_type,
                    "close": curr["close"],
                    "open":  curr["open"],
                    "high":  curr["high"],
                    "low":   curr["low"],
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

        except Exception as e:
            print(f"❌ Error {pair}: {e}")

if __name__ == "__main__":
    run_check()