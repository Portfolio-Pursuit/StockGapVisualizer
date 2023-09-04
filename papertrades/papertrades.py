# papertrades.papertrades.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from papertrades.models.papertrades import PaperTrade
from common.application.application import db
from common.auth.login_required import login_required
import yfinance as yf
import locale
from common.market.data.stocks import get_sp500_symbols

paper_trading_blueprint = Blueprint('paper_trading', __name__,  template_folder='templates',
    static_folder='static', static_url_path='assets')

locale.setlocale( locale.LC_ALL, '' )

@paper_trading_blueprint.route('/', methods=['GET'])
@login_required
def list_paper_trades():
    paper_trades = PaperTrade.query.all()
    current_stock_data = addStockData(paper_trades)
    return render_template('papertrades.html', paper_trades=paper_trades, current_stock_data=current_stock_data, sp500_symbols=get_sp500_symbols())

@paper_trading_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def create_paper_trade():
    if request.method == 'POST':
        asset = request.form['asset']
        direction = request.form['direction']
        quantity = int(request.form['quantity'])
        entry_price = float(request.form['entry_price'])
        
        # Calculate some trade-related values (e.g., timestamp)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Create a new PaperTrade object
        paper_trade = PaperTrade(
            asset=asset,
            direction=direction,
            quantity=quantity,
            entry_price=entry_price,
            timestamp=timestamp,
        )
        
        # Add the paper trade to the database
        db.session.add(paper_trade)
        db.session.commit()
        
        return redirect(url_for('paper_trading.list_paper_trades'))
    
    return render_template('create_paper_trades.html', sp500_symbols=get_sp500_symbols())

@paper_trading_blueprint.route('/remove/<int:trade_id>', methods=['POST'])
@login_required
def remove_paper_trade(trade_id):
    paper_trade = PaperTrade.query.get_or_404(trade_id)
    db.session.delete(paper_trade)
    db.session.commit()
    flash('Paper trade removed successfully', 'success')
    return redirect(url_for('paper_trading.list_paper_trades'))

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
