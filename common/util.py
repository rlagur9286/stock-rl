import os
import time
import datetime
import locale
import logging

import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Strategy
# DEBUG = True
DEBUG = False
DEMO = True
# DEMO = False
TRANSACTION_TERM = 2  # 2 seconds
PROCESSING_TERM = 2  # 2 seconds
MARKET_WAIT_TERM = 10  # 10 seconds
MAX_TARGET_STOCK_PRICE = 500000
MAX_BUY_PRICE_AGG = 1000000
MAX_BUY_PRICE_DEF = 500000
BUY_UNIT_AGG = 500000
BUY_UNIT_DEF = 100000
TGT_TOP_DIFF = 10
TGT_BOTTOM_DIFF = -3
MIN_PRICE_VOLUME = 10000 * 10000
# Number of Holdings
MAX_NUM_HOLDINGS_AGG = 12
MAX_NUM_HOLDINGS_DEF = 5
# MAX_NUM_HOLDINGS_DEF = 0
# Monitoring Stocks
MAX_STOCKS_MONITOR_ITR = 5 # Each of KOSDAQ and KOSPI
FIVEMIN_INCDEC_RATE = 0.025

# Date Time Format
FORMAT_DATE = "%Y%m%d"
FORMAT_DATETIME = "%Y%m%d%H%M%S"
timestr = datetime.datetime.fromtimestamp(int(time.time())).strftime(FORMAT_DATETIME)
