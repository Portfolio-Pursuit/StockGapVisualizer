# dashboard.watchlist.py

import yfinance as yf
from common.auth.login_required import login_required
from flask import render_template, Blueprint

watchlist_blueprint = Blueprint('watchlist', __name__, url_prefix= '/watchlist', template_folder='templates',
    static_folder='static', static_url_path='assets')

# TODO: figure out structure but Tola likes this
watchlist_blueprint_temp = Blueprint('watchlist', __name__, template_folder='templates',
    static_folder='static', static_url_path='assets')

@watchlist_blueprint_temp.route('/')
@watchlist_blueprint.route('/')
@login_required
def dashboard():
    return render_template('watchlist.html')

class WatchlistItem:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = self.fetch_stock_data()

    def fetch_stock_data(self):
        try:
            stock_info = yf.Ticker(self.ticker)
            data = stock_info.history(period="1d")  # Fetch today's data for demonstration
            if not data.empty:
                return {
                    "ticker": self.ticker,
                    "current_price": data["Close"][0],
                    "high_price": data["High"][0],
                    "low_price": data["Low"][0],
                }
            else:
                return None
        except Exception as e:
            print(f"Error fetching data for {self.ticker}: {str(e)}")
            return None

# Simulated user watchlist
user_watchlist = ["AAPL", "GOOGL", "TSLA", "MSFT"]

def get_watchlist_data():
    watchlist_data = []
    for ticker in user_watchlist:
        item = WatchlistItem(ticker)
        if item.data:
            watchlist_data.append(item.data)
    return watchlist_data

# Example usage
if __name__ == "__main__":
    watchlist_data = get_watchlist_data()
    for item in watchlist_data:
        print(f"Ticker: {item['ticker']}")
        print(f"Current Price: {item['current_price']}")
        print(f"High Price: {item['high_price']}")
        print(f"Low Price: {item['low_price']}")
        print("---")