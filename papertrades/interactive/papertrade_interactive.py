# papertrades.interactive.papertrade_interactive.py

from flask import Blueprint, request, jsonify
from datetime import datetime
from papertrades.interactive.models.papertrade_interactive import PaperTradeInteractive
from papertrades.interactive.models.currency_interactive import CurrencyInteractive, initCurrency
from common.application.application import db
from common.auth.login_required import login_required
import yfinance as yf
import locale
from common.market.data.stocks import get_sp500_symbols
from common.ui.navbar import navbar, getUIDir
from flask_login import current_user

renderEnv = navbar(getUIDir(__file__)).getEnv()

local_template = 'papertrades_interactive.html'
paper_trading_interactive_blueprint = Blueprint('paper_trading_interactive', __name__,  template_folder='templates',
    static_folder='static', static_url_path='assets')

locale.setlocale( locale.LC_ALL, '' )

@paper_trading_interactive_blueprint.route('/', methods=['GET'])
@login_required
def list_paper_trades():
    paper_trades = PaperTradeInteractive.query.filter_by(user_id=current_user.id).all()
    current_stock_data = addStockData(paper_trades)
    return renderEnv.get_template(local_template).render(paper_trades=paper_trades, 
            current_stock_data=current_stock_data, sp500_symbols=get_sp500_symbols(), total_currency=getTotalCurrency())

@paper_trading_interactive_blueprint.route('/new', methods=['POST'])
@login_required
def create_paper_trade():
    if request.method == 'POST':
        asset = request.json.get('asset')
        direction = request.json.get('direction')
        quantity = request.json.get('quantity')
        entry_price = request.json.get('entryPrice')

        cost = int(quantity) * float(entry_price)
        if int(quantity) <= 0:
            return 'Not valid quantity', 400
        if cost > getTotalCurrencyNoFormat():
            return 'Not enough total currency', 400

        paper_trade = PaperTradeInteractive(
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

        total_currency = formatCurrency(subtractFromTotalCurrency(cost))

        # Return the newly created paper trade data in JSON format
        return jsonify({'tradeId': paper_trade.id, 'timestamp': paper_trade.timestamp, 'total_currency': total_currency })

@paper_trading_interactive_blueprint.route('/remove/<int:trade_id>', methods=['POST'])
@login_required
def remove_paper_trade(trade_id):
    paper_trade = PaperTradeInteractive.query.get_or_404(trade_id)
    db.session.delete(paper_trade)
    db.session.commit()
    stock_data = get_stock_data_for_papertrade(paper_trade)
    is_buy = paper_trade.direction == "buy"
    if is_buy:
        profit = -1 * float(stock_data['market_value'])
    else: 
        profit = -1 * (float(stock_data['cost_basis'] + stock_data['gain_loss']))

    total_currency = formatCurrency(subtractFromTotalCurrency(profit))
    return jsonify({'total_currency': total_currency, 'message': 'Paper trade removed successfully'})

@paper_trading_interactive_blueprint.route('/get_stock_data/<int:trade_id>', methods=['GET'])
@login_required
def get_stock_data_for_trade(trade_id):
    # Get the PaperTradeInteractive object by trade_id
    paper_trade = PaperTradeInteractive.query.get_or_404(trade_id)
    stock_data = get_stock_data_for_papertrade(paper_trade)
    for key in stock_data.keys():
        stock_data[key] = formatCurrency(stock_data[key])
    return jsonify(stock_data)

def get_stock_data_for_papertrade(paper_trade):
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
        stock_data['current_price'] = current_price

        # Calculate gain/loss, price change, cost basis, and market value
        cost_basis = paper_trade.entry_price * paper_trade.quantity
        market_value = current_price * paper_trade.quantity
        price_change = current_price - paper_trade.entry_price
        is_buy = paper_trade.direction == "buy"
        gain_loss = (1 if is_buy else -1) * (market_value - cost_basis)

        stock_data['gain_loss'] = gain_loss
        stock_data['price_change'] = price_change
        stock_data['cost_basis'] = cost_basis
        stock_data['market_value'] = market_value

    except Exception as e:
        print(f"Error fetching stock data for {asset}: {str(e)}")
    return stock_data

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
                'current_price': formatCurrency(current_price),
                'gain_loss': formatCurrency(gain_loss), 
                'price_change': formatCurrency(price_change), 
                'cost_basis': formatCurrency(cost_basis), 
                'market_value': formatCurrency(market_value), 
            }
    return paper_trades_to_stock_data

def getTotalCurrency():
    currency = getTotalCurrencyNoFormat()
    if not currency:
        initCurrency(current_user)
        currency = getTotalCurrencyNoFormat()
    return formatCurrency(currency)

def formatCurrency(currency):
    return locale.currency(currency, grouping=True)

def getTotalCurrencyNoFormat():
    return CurrencyInteractive.query.filter_by(user_id=current_user.id).first().total_currency

def subtractFromTotalCurrency(cost):
    user_currency = CurrencyInteractive.query.filter_by(user_id=current_user.id).first()
    
    if user_currency:
        user_currency.total_currency -= cost
        db.session.commit()
        return user_currency.total_currency 
    else:
        raise Exception("User currency data not found")
        return 'Unknown'
    
# Define the stock or ETF symbol for which you want to retrieve option data
symbol = "AAPL"  # Example: Apple Inc.

# Create a Yahoo Finance ticker object
stock = yf.Ticker(symbol)

# Get the option chain for the selected stock
option_chain = stock.option_chain()

# Access call and put option data
calls = option_chain.calls
puts = option_chain.puts

# Display the option chain data
print("Call Options:")
print(calls.head())

print("\nPut Options:")
print(puts.head())