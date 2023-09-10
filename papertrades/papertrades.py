# papertrades.papertrades.py

from flask import Blueprint, request, flash, jsonify
from datetime import datetime
from papertrades.models.papertrades import PaperTrade
from common.application.application import db
from common.auth.login_required import login_required
import yfinance as yf
import locale
from common.market.data.stocks import get_sp500_symbols
from common.ui.navbar import navbar, getUIDir
from flask_login import current_user

renderEnv = navbar(getUIDir(__file__)).getEnv()

local_template = 'papertrades.html'
paper_trading_blueprint = Blueprint('paper_trading', __name__,  template_folder='templates',
    static_folder='static', static_url_path='assets')

locale.setlocale( locale.LC_ALL, '' )

@paper_trading_blueprint.route('/', methods=['GET'])
@login_required
def list_paper_trades():
    paper_trades = PaperTrade.query.filter_by(user_id=current_user.id).all()
    current_stock_data = addStockData(paper_trades)
    return renderEnv.get_template(local_template).render(paper_trades=paper_trades, current_stock_data=current_stock_data, sp500_symbols=get_sp500_symbols())

@paper_trading_blueprint.route('/new', methods=['POST'])
@login_required
def create_paper_trade():
    if request.method == 'POST':
        asset = request.json.get('asset')
        direction = request.json.get('direction')
        quantity = request.json.get('quantity')
        entry_price = request.json.get('entryPrice')

        paper_trade = PaperTrade(
            user_id=current_user.id,
            asset=asset,
            direction=direction,
            quantity=quantity,
            entry_price=entry_price,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )

        # Add the paper trade to the database
        db.session.add(paper_trade)
        db.session.commit()

        # Return the newly created paper trade data in JSON format
        return jsonify({'tradeId': paper_trade.id, 'timestamp': paper_trade.timestamp})

@paper_trading_blueprint.route('/remove/<int:trade_id>', methods=['POST'])
@login_required
def remove_paper_trade(trade_id):
    paper_trade = PaperTrade.query.get_or_404(trade_id)
    db.session.delete(paper_trade)
    db.session.commit()
    flash('Paper trade removed successfully', 'success')
    return jsonify({'message': 'Paper trade removed successfully'})

@paper_trading_blueprint.route('/get_stock_data/<int:trade_id>', methods=['GET'])
@login_required
def get_stock_data_for_trade(trade_id):
    # Get the PaperTrade object by trade_id
    paper_trade = PaperTrade.query.get_or_404(trade_id)

    # Get the asset symbol for the trade
    asset = paper_trade.asset

    # Define a dictionary to hold the stock data
    stock_data = {
        'current_price': 'Unknown',
        'gain_loss': 'Unknown',
        'price_change': 'Unknown',
        'cost_basis': 'Unknown',
        'market_value': 'Unknown',
    }

    try:
        # Fetch the current price for the asset
        stock_info = yf.Ticker(asset)
        current_price = stock_info.history(period="1d")["Close"].iloc[0]

        if not current_price:
            raise Exception("Current price not available")

        current_price = round(current_price, 2)
        stock_data['current_price'] = locale.currency(current_price, grouping=True)

        # Calculate gain/loss, price change, cost basis, and market value
        cost_basis = paper_trade.entry_price * paper_trade.quantity
        market_value = current_price * paper_trade.quantity
        price_change = current_price - paper_trade.entry_price
        is_buy = paper_trade.direction == "buy"
        gain_loss = (1 if is_buy else -1) * (market_value - cost_basis)

        stock_data['gain_loss'] = locale.currency(gain_loss, grouping=True)
        stock_data['price_change'] = locale.currency(price_change, grouping=True)
        stock_data['cost_basis'] = locale.currency(cost_basis, grouping=True)
        stock_data['market_value'] = locale.currency(market_value, grouping=True)

    except Exception as e:
        print(f"Error fetching stock data for {asset}: {str(e)}")

    return jsonify(stock_data)

def addStockData(paper_trades):
    paper_trades_to_stock_data = {}
    tickersToPriceMap = {}
    for trade in paper_trades:
        asset = trade.asset
        tickersToPriceMap[asset] = {
            'current_price': 'Unknown',
        }
        paper_trades_to_stock_data[trade.id] = {
            'current_price': 'Unknown',
            'gain_loss': 'Unknown',
            'price_change': 'Unknown',
            'cost_basis': 'Unknown',
            'market_value': 'Unknown',
        }
    for ticker in tickersToPriceMap.keys():
        try:
            stock_info = yf.Ticker(ticker)
            current_price = stock_info.history(period="1d")["Close"].iloc[0]
            if current_price != 'Unknown':
                current_price = round(current_price, 2)
                tickersToPriceMap[ticker]['current_price'] = current_price
        except:
            pass
    for trade in paper_trades:
        current_price = tickersToPriceMap[trade.asset]['current_price']
        if current_price != 'Unknown':
            cost_basis = trade.entry_price * trade.quantity
            market_value = current_price * trade.quantity
            price_change = current_price - trade.entry_price
            isBuy = trade.direction == "buy"
            gain_loss = (1 if isBuy else -1) * (market_value - cost_basis)
            paper_trades_to_stock_data[trade.id] = {
                'current_price': locale.currency(current_price, grouping=True),
                'gain_loss': locale.currency(gain_loss, grouping=True), 
                'price_change': locale.currency(price_change, grouping=True), 
                'cost_basis': locale.currency(cost_basis, grouping=True), 
                'market_value': locale.currency(market_value, grouping=True), 
            }
    return paper_trades_to_stock_data
