import yfinance as yf
import sqlite3
import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import keyring
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
    conn = sqlite3.connect("StockData.db")
    # conn2 = sqlite3.connect("/Users/afaqnabi/PycharmProjects/TradingBot/StockData(1d).db")
    # cursor2 = conn2.cursor()
    cursor = conn.cursor()

    all_stocks = scrape_watchlist()
    for symbol in all_stocks:
        if is_new(symbol, cursor, conn) is True:
            # insert_data_for_new_stock_1d(symbol, conn, cursor)
            insert_data_for_new_stock_5m(symbol, conn, cursor)
        else:
            try:
                # data = yf.download(tickers=symbol, period="max", interval="1d", debug=False)
                # data.to_sql(name=symbol, con=conn, if_exists='append', index=True)
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
    with open('All_Stocks.csv') as csv_file:
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


def scrape_watchlist():
    service = "login"
    info = "info"
    DRIVER_PATH = '/Users/afaqnabi/PycharmProjects/TradingBot/chromedriver'
    url = "https://login.yahoo.com/?.src=fpctx&.intl=ca&.lang=en-CA&.done=https://ca.yahoo.com&activity=uh-signin&pspid=2142623533"
    finURL = "https://ca.finance.yahoo.com/portfolio/p_1/view/v2"
    username = keyring.get_password(service, info)
    password = keyring.get_password(service, username)
    options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    driver.maximize_window()
    sleep(3)
    driver.find_element_by_xpath('//*[@id="login-username"]').send_keys(username)
    sleep(3)
    driver.find_element_by_xpath('//*[@id="login-username"]').send_keys(Keys.RETURN)
    sleep(3)
    driver.find_element_by_xpath('//*[@id="login-passwd"]').send_keys(password)
    sleep(5)
    wait.until(EC.presence_of_element_located((By.ID, 'login-passwd'))).send_keys(Keys.RETURN)
    sleep(5)
    driver.get(finURL)
    sleep(3)
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html, 'html.parser')
    prev_symbols = set(get_symbols())
    new = set()
    for i in soup.find_all('a'):
        x = i.get("href")
        if "quote" in x:
            string = "p="
            new.add(x[x.index(string) + len(string):])
    symbols = set.union(prev_symbols, new)

    return list(symbols)


if __name__ == '__main__':
    main()
