# --------------------------------------------------
# ORB Settings
# --------------------------------------------------

ORB_WINDOW_MINUTES = 15

BREAKOUT_BUFFER_POINTS = 5


# --------------------------------------------------
# Stop Loss Settings
# --------------------------------------------------

# Maximum SL override (%)
STOP_LOSS_PERCENT = 0.5

# Future SL modes:
# "ORB"
# "PERCENT"
STOP_LOSS_TYPE = "ORB"


# --------------------------------------------------
# Option Selling Settings
# --------------------------------------------------

# How far OTM to sell
OPTION_OTM_DISTANCE = 100

# Expiry type
# "CURRENT"
# "NEXT"
EXPIRY_TYPE = "CURRENT"


# --------------------------------------------------
# Trade Direction Settings
# --------------------------------------------------

ALLOW_LONG = True
ALLOW_SHORT = True


# --------------------------------------------------
# Trade Timing
# --------------------------------------------------

MARKET_OPEN_TIME = "09:15:00"

LAST_ENTRY_TIME = "14:30:00"

FORCE_EXIT_TIME = "15:25:00"


# --------------------------------------------------
# Risk Management
# --------------------------------------------------

CAPITAL = 300000

RISK_PER_TRADE_PERCENT = 2.0

MAX_TRADES_PER_DAY = 2

# --------------------------------------------------
# Trade Size
# --------------------------------------------------
TRADE_LOT = 1
LOT_SIZE = 65

# --------------------------------------------------
# Output Settings
# --------------------------------------------------

SAVE_TRADES = True

SAVE_DAILY_SUMMARY = True

SAVE_EQUITY_CURVE = True

# Entry timeframe
ENTRY_TIMEFRAME = "5min"

# Exit timeframe
EXIT_TIMEFRAME = "1min"

# --------------------------------------------------
# Re-entry Behavior
# --------------------------------------------------

# Re-entry behavior
REENTRY_MODE = "ANY"

# Options:
# "ANY"
# "OPPOSITE_ONLY"
# "NONE"

# --------------------------------------------------
# Trade Type Tag
# --------------------------------------------------

TRADE_TYPE = "ORB"

# --------------------------------------------------
# Trend Filter
# --------------------------------------------------

USE_TREND_FILTER = True

DAILY_EMA_PERIOD = 50

# --------------------------------------------------
# ORB Range Filter
# --------------------------------------------------

USE_ORB_RANGE_FILTER = True

MIN_ORB_RANGE = 50

# --------------------------------------------------
# ATR Volatility Filter
# --------------------------------------------------

USE_ATR_FILTER = False

ATR_PERIOD = 14

ATR_TIMEFRAME = "D"   # Daily ATR

MIN_ATR_MULTIPLIER = 0.3