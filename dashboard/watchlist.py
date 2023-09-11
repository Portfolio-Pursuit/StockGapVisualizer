# Import necessary modules
import yfinance as yf
from flask import Blueprint, render_template, request, redirect, url_for
from common.auth.login_required import login_required
from common.application.application import db
from common.market.data.stocks import current_price
from common.ui.navbar import navbar, getUIDir
from flask_login import current_user

# Import the Watchlist model from your watchlist_models module
from dashboard.models.watchlist_models import Watchlist  # Adjust the import path as needed

# Create a Blueprint for the watchlist
watchlist_blueprint = Blueprint('watchlist', __name__, static_folder='static', static_url_path='assets')

renderEnv = navbar(getUIDir(__file__)).getEnv()
local_template = 'watchlist.html'

# Sample stocks for the watchlist
watchlist_stocks = ["AAPL", "GOOGL", "TSLA", "MSFT", "AMZN"]

# Route for displaying the watchlist
@watchlist_blueprint.route('/')
@login_required  
def display_watchlist():
    # Query the user's watchlist from the database (example query)
    user_watchlist = Watchlist.query.filter_by(user_id=current_user.id).all()

    # Create a list of stock symbols from the user's watchlist
    watchlist_stocks_saved = [item.asset for item in user_watchlist]
    if watchlist_stocks_saved and len(watchlist_stocks_saved) > 0:
        watchlist_stocks = watchlist_stocks_saved

    watchlist_data = []

    for ticker in watchlist_stocks:
        watchlist_data.append({
            "ticker": ticker,
            "current_price": current_price(ticker),
        })

    return renderEnv.get_template(local_template).render(watchlist_data=watchlist_data)

# Route for adding a new stock to the watchlist
@watchlist_blueprint.route('/add_stock', methods=['POST'])
@login_required
def add_stock():
    new_stock_symbol = request.form.get('newStockSymbol')
    
    if new_stock_symbol:
        try:
            stock_info = yf.Ticker(new_stock_symbol)
            data = stock_info.history(period="1d")  # Fetch today's data for demonstration
            if not data.empty:
                # Create a new Watchlist item for the user
                new_watchlist_item = Watchlist(user_id=current_user.id, asset=new_stock_symbol)
                db.session.add(new_watchlist_item)
                db.session.commit()

                # Fetch the current price and update the new_watchlist_item
                new_watchlist_item.current_price = current_price(new_stock_symbol)
                db.session.commit()
        except Exception as e:
            print(f"Error adding new stock {new_stock_symbol}: {str(e)}")

    return redirect(url_for('watchlist.display_watchlist'))

