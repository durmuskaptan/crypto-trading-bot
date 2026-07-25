# Zafer Bot v3 Configuration
import os
from dotenv import load_dotenv

load_dotenv()

# ========== BINANCE & TELEGRAM ==========
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET', '')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '7728593511:AAHwaFzQNIbbidHs-C2Mv48OdI5q-IQlkvk')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '7135551119')

# ========== TRADING PARAMETERS ==========
SYMBOLS = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "AVAX/USDT", "XRP/USDT"]
INITIAL_BALANCE = 1000.0
MAX_POSITION_SIZE_PERCENT = 0.25  # Her pozisyon max %25 bakiye
MAX_CONCURRENT_POSITIONS = 3
SCAN_INTERVAL = 15  # Saniye

# ========== RISK MANAGEMENT ==========
STOP_LOSS_ATR_MULTIPLIER = 2.0
TAKE_PROFIT_LEVELS = [0.10, 0.25, 0.50]  # %10, %25, %50
PARTIAL_TAKE_PROFIT = [0.5, 0.3, 0.2]  # Parçalı satış
DCA_MAX_COUNT = 3
DCA_THRESHOLD = -5.0  # -5% düşüşte DCA
DCA_MULTIPLIER = 1.5  # 1.5x orjinal miktarı ekleme

# ========== STRATEGY PARAMETERS ==========
RSI_PERIOD = 14
RSI_OVERSOLD = 32
RSI_OVERBOUGHT = 65
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BB_PERIOD = 20
BB_STD = 2
ATR_PERIOD = 14

# ========== ADVANCED FEATURES ==========
USE_ML_PREDICTION = True
USE_GRID_TRADING = True
USE_CORRELATION_FILTER = True
USE_VOLATILITY_ADJUSTMENT = True
USE_SWING_DETECTION = True

# ========== TIMEFRAMES ==========
MAIN_TIMEFRAME = "1h"
SECONDARY_TIMEFRAME = "4h"
TERTIARY_TIMEFRAME = "15m"

# ========== MONEY MANAGEMENT ==========
KELLY_FRACTION = 0.25  # Kelly Criterion'ın %25'i (güvenli)
USE_KELLY_SIZING = True

# ========== DATABASE ==========
DB_PATH = "zafer_bot.db"
ENABLE_BACKTEST_DB = True

# ========== TRADING MODE ==========
PAPER_TRADING = False  # True = Test Mode, False = Real Trading
MIN_VOLUME_MULTIPLIER = 1.3  # Hacim en az SMA'nın 1.3x olmalı

# ========== PERFORMANCE TRACKING ==========
TRACK_TRADES = True
GENERATE_DAILY_REPORT = True
REPORT_TIME = "22:00"  # Saat formatında

# ========== LOGGING ==========
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_TO_FILE = True
LOG_FILE = "zafer_bot.log"
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
