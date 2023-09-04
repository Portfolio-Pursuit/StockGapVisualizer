# common.market.data.stocks.py

import pandas as pd

def get_sp500_symbols():
    try:
        sp500_data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        sp500_symbols = sp500_data['Symbol'].tolist()
        return sp500_symbols
    except Exception as e:
        print(f"Error retrieving S&P 500 symbols: {str(e)}")
        return []
