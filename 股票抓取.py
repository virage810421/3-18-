import yfinance as yf
import pyodbc
import time
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

# 🔁 每35秒存一次
while True:
    try:
        save_stock("2330.TW")
        save_stock("2345.TW")

    except Exception as e:
        print("錯誤:", e)

    time.sleep(35)