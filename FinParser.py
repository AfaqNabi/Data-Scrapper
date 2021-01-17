import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.layers import LSTM
# from keras.layers import Dropout
import itertools as it
import time
import schedule

def main():
    # i=0
    print("test")
    # i+=1
    # global conn
    # global cursor
    # conn = sqlite3.connect("StockData.db")
    # cursor = conn.cursor()


if __name__ == '__main__':
    schedule.every().day.at("02:30").do(main)
    while True:
        schedule.run_pending()