# common.market.data.stocks.py

import pandas as pd
import yfinance as yf

def get_sp500_symbols():
    try:
        sp500_data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        sp500_symbols = sp500_data['Symbol'].tolist()
        return sp500_symbols
    except Exception as e:
        print(f"Error retrieving S&P 500 symbols: {str(e)}")
        return []

def get_current_price(symbol):
    stock_info = yf.Ticker(symbol)
    try:
        current_price = stock_info.history(period="1d")["Close"].iloc[0]
        current_price = round(current_price, 2)
    except:
        current_price = 'Unknown'
    return current_price