from config import SUPPORT_RESISTANCE

def check_near_level(price: float, levels: list, threshold_pips: float = 0.0015) -> dict:
    """เช็คว่าราคาใกล้แนวรับ/แนวต้านไหม"""
    for level in levels:
        distance = abs(price - level)
        distance_pct = distance / level
        if distance_pct <= threshold_pips:
            return {"near": True, "level": level, "distance_pips": round(distance * 100, 1)}
    return {"near": False}

def analyze_engulfing_signal(data: dict) -> dict:
    """
    วิเคราะห์ Engulfing Candle บน TF 15M
    data จาก TradingView alert:
    {
        "pair": "USDJPY",
        "candle_type": "bullish_engulfing" | "bearish_engulfing",
        "close": 150.75,
        "open": 150.60,
        "high": 150.80,
        "low": 150.55,
        "prev_close": 150.50,
        "prev_open": 150.65,
        "trend_4h": "bullish" | "bearish",
        "trend_1d": "bullish" | "bearish",
    }
    """
    pair = data.get("pair")
    price = data.get("close")
    candle_type = data.get("candle_type")
    
    if pair not in SUPPORT_RESISTANCE:
        return {"valid": False, "reason": "Pair not supported"}

    sr = SUPPORT_RESISTANCE[pair]
    result = {
        "valid": False,
        "pair": pair,
        "candle_type": candle_type,
        "price": price,
        "signal": None,
        "confluence": [],
        "strength": 0,
        "near_level": None,
    }

    # === เช็ค Bullish Engulfing → สัญญาณ BUY ===
    if candle_type == "bullish_engulfing":
        for tf in ["15M", "2H", "4H", "1D", "1W"]:
            check = check_near_level(price, sr[tf]["support"])
            if check["near"]:
                result["confluence"].append(f"✅ ใกล้ Support {tf}: {check['level']}")
                result["strength"] += (1 if tf == "15M" else 2 if tf in ["2H","4H"] else 3)
                if not result["near_level"]:
                    result["near_level"] = check["level"]

        if result["confluence"]:
            result["valid"] = True
            result["signal"] = "BUY"

    # === เช็ค Bearish Engulfing → สัญญาณ SELL ===
    elif candle_type == "bearish_engulfing":
        for tf in ["15M", "2H", "4H", "1D", "1W"]:
            check = check_near_level(price, sr[tf]["resistance"])
            if check["near"]:
                result["confluence"].append(f"🚫 ใกล้ Resistance {tf}: {check['level']}")
                result["strength"] += (1 if tf == "15M" else 2 if tf in ["2H","4H"] else 3)
                if not result["near_level"]:
                    result["near_level"] = check["level"]

        if result["confluence"]:
            result["valid"] = True
            result["signal"] = "SELL"

    # คำนวณ SL/TP แบบง่าย
    if result["valid"]:
        candle_range = abs(data.get("high", price) - data.get("low", price))
        sl_pips = round(candle_range * 1.5, 5)
        tp_pips = round(candle_range * 2.5, 5)
        
        if result["signal"] == "BUY":
            result["sl"] = round(price - sl_pips, 5)
            result["tp1"] = round(price + tp_pips, 5)
            result["tp2"] = round(price + tp_pips * 2, 5)
        else:
            result["sl"] = round(price + sl_pips, 5)
            result["tp1"] = round(price - tp_pips, 5)
            result["tp2"] = round(price - tp_pips * 2, 5)

        result["rr_ratio"] = round(tp_pips / sl_pips, 2)

    return result