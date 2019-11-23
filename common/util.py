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

headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'GS_font_Name_no=0; GS_font_size=16; _ga=GA1.3.937989519.1493034297; webid=bb619e03ecbf4672b8d38a3fcedc3f8c; _ga=GA1.2.937989519.1493034297; _gid=GA1.2.215330840.1541556419; KAKAO_STOCK_RECENT=[%22A069500%22]; recentMenus=[{%22destination%22:%22chart%22%2C%22title%22:%22%EC%B0%A8%ED%8A%B8%22}%2C{%22destination%22:%22current%22%2C%22title%22:%22%ED%98%84%EC%9E%AC%EA%B0%80%22}]; TIARA=C-Tax5zAJ3L1CwQFDxYNxe-9yt4xuvAcw3IjfDg6hlCbJ_KXLZZhwEPhrMuSc5Rv1oty5obaYZzBQS5Du9ne5x7XZds-vHVF; webid_sync=1541565778037; _gat_gtag_UA_128578811_1=1; _dfs=VFlXMkVwUGJENlVvc1B3V2NaV1pFdHhpNTVZdnRZTWFZQWZwTzBPYWRxMFNVL3VrODRLY1VlbXI0dHhBZlJzcE03SS9Vblh0U2p2L2V2b3hQbU5mNlE9PS0tcGI2aXQrZ21qY0hFbzJ0S1hkaEhrZz09--6eba3111e6ac36d893bbc58439d2a3e0304c7cf3',
        'Host': 'finance.daum.net',
        'If-None-Match': 'W/"23501689faaaf24452ece4a039a904fd"',
        'Referer': 'http://finance.daum.net/quotes/A069500',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }