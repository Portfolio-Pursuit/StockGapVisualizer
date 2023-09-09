# dashboard.watchlist.py

import yfinance as yf
from common.auth.login_required import login_required
from common.market.data.stocks import current_price
from flask import Blueprint, Flask, request
from common.ui.navbar import navbar, getUIDir

renderEnv = navbar(getUIDir(__file__)).getEnv()

watchlist_blueprint = Blueprint('watchlist_temp', __name__, url_prefix= '/watchlist', static_folder='static', static_url_path='assets')
local_template = 'watchlist.html'

# Sample stocks for the watchlist
watchlist_stocks = ["AAPL", "GOOGL", "TSLA", "MSFT", "AMZN"]

@watchlist_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def watchlist():
    global watchlist_stocks
    watchlist_data = []

    # if request.method == 'POST':
    #     new_stock_symbol = request.form.get('newStockSymbol')
    #     if new_stock_symbol:
    #         try:
    #             stock_info = yf.Ticker(new_stock_symbol)
    #             data = stock_info.history(period="1d")  # Fetch today's data for demonstration
    #             if not data.empty:
    #                 watchlist_stocks.append(new_stock_symbol)
    #         except Exception as e:
    #             print(f"Error adding new stock {new_stock_symbol}: {str(e)}")

    for ticker in watchlist_stocks:
        watchlist_data.append({
            "ticker": ticker,
            "current_price": current_price(ticker),
        })
    return renderEnv.get_template(local_template).render(watchlist_data=watchlist_data)
