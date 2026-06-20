import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN   = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
TRADINGVIEW_SECRET  = os.getenv("TRADINGVIEW_SECRET")

PAIRS = ["USDJPY", "GBPUSD", "GBPJPY"]

# แนวรับ/แนวต้านแต่ละ TF (อัปเดตเองตาม TradingView)
SUPPORT_RESISTANCE = {
    "USDJPY": {
        "1W":  {"support": [148.00, 145.00], "resistance": [155.00, 158.00]},
        "1D":  {"support": [149.50, 148.80], "resistance": [153.00, 154.50]},
        "4H":  {"support": [150.20, 149.80], "resistance": [151.50, 152.00]},
        "2H":  {"support": [150.50, 150.20], "resistance": [151.00, 151.30]},
        "15M": {"support": [150.60, 150.45], "resistance": [150.85, 151.00]},
    },
    "GBPUSD": {
        "1W":  {"support": [1.2400, 1.2200], "resistance": [1.2900, 1.3100]},
        "1D":  {"support": [1.2580, 1.2520], "resistance": [1.2750, 1.2820]},
        "4H":  {"support": [1.2620, 1.2600], "resistance": [1.2700, 1.2730]},
        "2H":  {"support": [1.2640, 1.2625], "resistance": [1.2680, 1.2700]},
        "15M": {"support": [1.2650, 1.2640], "resistance": [1.2670, 1.2680]},
    },
    "GBPJPY": {
        "1W":  {"support": [185.00, 182.00], "resistance": [192.00, 195.00]},
        "1D":  {"support": [188.00, 187.00], "resistance": [191.00, 192.00]},
        "4H":  {"support": [188.50, 188.00], "resistance": [190.00, 190.50]},
        "2H":  {"support": [188.80, 188.50], "resistance": [189.50, 189.80]},
        "15M": {"support": [189.00, 188.90], "resistance": [189.30, 189.50]},
    },
}