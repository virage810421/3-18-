import yfinance as yf
import pyodbc
import time
import random
from datetime import datetime

# 🔌 資料庫連線
server = "localhost"   # 改成你的 SQL Server
database = "股票爬蟲"

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

def save_stock(stock_id):
    tick = yf.Ticker(stock_id)
    info = tick.fast_info

    price = info.get("lastPrice")
    open_p = info.get("open")
    high = info.get("dayHigh")
    low = info.get("dayLow")

    print(f"{datetime.now()} | {stock_id} | {price}")

    # 📝 寫入資料庫
    cursor.execute("""
        INSERT INTO StockPrices (StockId, Price, OpenPrice, HighPrice, LowPrice)
        VALUES (?, ?, ?, ?, ?)
    """, stock_id, price, open_p, high, low)

    conn.commit()

# 🔁 平日隨機間隔抓取，只在指定時間範圍執行
while True:
    now = datetime.now()
    # 平日判斷：0=Monday, 1=Tuesday, ..., 6=Sunday
    if now.weekday() < 5:  # 週一到週五
        # 設定抓取時間範圍（這裡示範 14:47 ~ 14:48，可改成你要的）
        start_time = now.replace(hour=15, minute=1, second=0, microsecond=0)
        end_time = now.replace(hour=15, minute=4, second=0, microsecond=0)

        if start_time <= now < end_time:
            try:
                save_stock("2330.TW")
                save_stock("2345.TW")
            except Exception as e:
                print("錯誤:", e)

            # 🔹 隨機間隔 2~10 秒
            interval = random.uniform(2, 10)
            time.sleep(interval)
        else:
            # 非抓取時間，休眠60秒再檢查
            time.sleep(60)
    else:
        # 週末，休眠1小時再檢查
        time.sleep(3600)