import yfinance as yf
import schedule
import time
import sys
from signal_analyzer import analyze_engulfing_signal
from bot import send_signal_to_discord

# Map ชื่อคู่เงินให้ตรงกับ yfinance
PAIR_SYMBOLS = {
    "USDJPY": "USDJPY=X",
    "GBPUSD": "GBPUSD=X",
    "GBPJPY": "GBPJPY=X",
}

def get_candles(symbol: str, period="1d", interval="15m"):
    """ดึงข้อมูลแท่งเทียน 15 นาทีจาก Yahoo Finance"""
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)
    return df

def check_engulfing(df):
    """เช็ค Engulfing จาก 2 แท่งล่าสุด"""
    if len(df) < 2:
        return None
    
    prev = df.iloc[-2]  # แท่งก่อนหน้า
    curr = df.iloc[-1]  # แท่งปัจจุบัน
    
    prev_body = prev["Close"] - prev["Open"]
    curr_body = curr["Close"] - curr["Open"]
    
    # Bullish Engulfing
    if (prev_body < 0 and curr_body > 0 and
        curr["Open"] < prev["Close"] and
        curr["Close"] > prev["Open"]):
        return "bullish_engulfing"
    
    # Bearish Engulfing
    if (prev_body > 0 and curr_body < 0 and
        curr["Open"] > prev["Close"] and
        curr["Close"] < prev["Open"]):
        return "bearish_engulfing"
    
    return None

def run_check():
    """รันการตรวจสอบทุกคู่เงิน"""
    print(f"🔍 Checking pairs...")
    
    for pair, symbol in PAIR_SYMBOLS.items():
        try:
            df = get_candles(symbol)
            candle_type = check_engulfing(df)
            
            if candle_type:
                curr = df.iloc[-1]
                prev = df.iloc[-2]
                
                data = {
                    "pair": pair,
                    "candle_type": candle_type,
                    "close": round(curr["Close"], 5),
                    "open": round(curr["Open"], 5),
                    "high": round(curr["High"], 5),
                    "low": round(curr["Low"], 5),
                    "prev_close": round(prev["Close"], 5),
                    "prev_open": round(prev["Open"], 5),
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
            print(f"❌ Error checking {pair}: {e}")

# รันทุก 15 นาที
schedule.every(15).minutes.do(run_check)

if __name__ == "__main__":
    if "--once" in sys.argv:
        run_check()   # รันครั้งเดียวแล้วจบ (สำหรับ GitHub Actions)
    else:
        print("🚀 Forex Alert Bot started!")
        run_check()
        while True:
            schedule.run_pending()
            time.sleep(60)