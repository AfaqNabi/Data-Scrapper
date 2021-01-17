import yfinance as yf
import sqlite3
import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
# import selenium
import time
import schedule
# import technical_indicators_lib
# use "period" instead of start/end
#     # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
#     # (optional, default is '1mo')
#     period='1mo',
#
#     # fetch data by interval (including intraday if period < 60 days)
#     # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
#     # (optional, default is '1d')
#     interval="5m",


def main():
    conn = sqlite3.connect("/Users/afaqnabi/PycharmProjects/TradingBot/StockData.db")
    conn2 = sqlite3.connect("/Users/afaqnabi/PycharmProjects/TradingBot/StockData(1d).db")
    cursor2 = conn2.cursor()
    cursor = conn.cursor()

    all_stocks = get_symbols()
    for symbol in all_stocks:
        if is_new(symbol, cursor, conn) is True:
            insert_data_for_new_stock_5m(symbol, conn, cursor)
        else:
            try:
                data_5m = yf.download(tickers=symbol, period='1d', interval="5m", debug=False)
                data_5m.to_sql(name=symbol, con=conn, if_exists='append', index=True)
            except Exception:
                print("Error: Unique Key constraint failed, error is ignored and nothing added to DB(5m): " + symbol)


def delete(date, all_stocks, cursor, conn, canadian=False):
    for symbol in all_stocks:
        if not canadian:
            x = "Delete from " + "`" + symbol + "`" + " where Datetime like "
            y = "'%" + date + "%'"
            z = x + str(y)
            cursor.execute(z)
            conn.commit()


def get_symbols():
    all = []
    with open('/Users/afaqnabi/PycharmProjects/TradingBot/All_Stocks.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            all.append(row[0])
            line_count += 1
    return all


def make_tables(cursor, conn, all_stocks):
    table = "CREATE TABLE IF NOT EXISTS "
    attributes = "(Datetime TEXT , Open REAL, High REAL, Low REAL, Close REAL, `Adj Close` REAL, Volume INTEGER, " \
                 "PRIMARY KEY('Datetime'))"
    for symbol in all_stocks:
        symbol = table + '`' + symbol + '`' + attributes
        cursor.execute(symbol)


def make_1d_tables(cursor, conn, all_stocks):
    table = "CREATE TABLE IF NOT EXISTS "
    attributes = "(Date TEXT , Open REAL, High REAL, Low REAL, Close REAL, `Adj Close` REAL, Volume INTEGER, " \
                 "PRIMARY KEY('Date'))"

    for symbol in all_stocks:
        symbol = table + '`' + symbol + '`' + attributes
        cursor.execute(symbol)


def is_new(symbol, cursor, conn):
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type = 'table' AND name = :symbol
        """, {'symbol': symbol})
    conn.commit()
    exists = cursor.fetchall()

    if not exists:
        return True
    else:
        return False


def insert_data_for_new_stock_5m(symbol, conn, cursor):
    table = "CREATE TABLE IF NOT EXISTS " + '`' + symbol + '`'
    attributes = "(Datetime TEXT , Open REAL, High REAL, Low REAL, Close REAL, `Adj Close` REAL, Volume INTEGER, PRIMARY KEY('Datetime'))"
    create = table + attributes
    cursor.execute(create)

    today = datetime.today()
    twomonthsBefore = today + relativedelta(days=-55)
    data = yf.download(tickers=symbol, start=twomonthsBefore, end=today, interval="5m", debug=False)
    try:
        data.to_sql(name=symbol, con=conn, if_exists='append', index=True)
    except Exception:
        print("Error: Unique Key constraint failed, error is ignored and nothing added to DB(5m): " + symbol)


def insert_data_for_new_stock_1d(symbol, conn, cursor):
    table = "CREATE TABLE IF NOT EXISTS " + '`' + symbol + '`'
    attributes = "(Date TEXT , Open REAL, High REAL, Low REAL, Close REAL, `Adj Close` REAL, Volume INTEGER, PRIMARY KEY('Date'))"
    create = table + attributes
    cursor.execute(create)

    data = yf.download(tickers=symbol, period="max", interval="1d", debug=False)
    try:
        data.to_sql(name=symbol, con=conn, if_exists='append', index=True)
    except Exception:
        print("Error: Unique Key constraint failed, error is ignored and nothing added to DB(1d): " + symbol)


if __name__ == '__main__':
    main()
