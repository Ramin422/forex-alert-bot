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
        "1W":  {"support": [155.02, 155.10], "resistance": [161.80, 161.78]},
        "1D":  {"support": [159.56, 159.60], "resistance": [161.80, 161.78]},
        "4H":  {"support": [160.48, 160.50], "resistance": [161.80, 161.78]},
        "2H":  {"support": [160.48, 160.50], "resistance": [161.80, 161.78]},
        "15M": {"support": [161.23, 161.25], "resistance": [161.80, 161.78]},
    },
    "GBPUSD": {
        "1W":  {"support": [1.31595, 1.31624], "resistance": [1.36581, 1.36570]},
        "1D":  {"support": [1.33051, 1.33061], "resistance": [1.34830, 1.34820]},
        "4H":  {"support": [1.33903, 1.33913], "resistance": [1.34445, 1.34435]},
        "2H":  {"support": [1.31640, 1.31650], "resistance": [1.32408, 1.32392]},
        "15M": {"support": [1.32137, 1.32147], "resistance": [1.32384, 1.32374]},
    },
    "GBPJPY": {
        "1W":  {"support": [206.651, 206.661], "resistance": [216.597, 216.587]},
        "1D":  {"support": [212.931, 212.941], "resistance": [215.607, 215.597]},
        "4H":  {"support": [212.404, 212.414], "resistance": [215.560, 215.550]},
        "2H":  {"support": [212.404, 212.414], "resistance": [213.575, 213.565]},
        "15M": {"support": [213.352, 213.354], "resistance": [213.554, 213.552]},
    },
}