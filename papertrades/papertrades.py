from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from papertrades.models.papertrades import PaperTrade
from common.application.application import db

paper_trading_blueprint = Blueprint('paper_trading', __name__,  template_folder='templates',
    static_folder='static', static_url_path='assets')

@paper_trading_blueprint.route('/', methods=['GET'])
def list_paper_trades():
    paper_trades = PaperTrade.query.all()
    return render_template('papertrades.html', paper_trades=paper_trades)

@paper_trading_blueprint.route('/new', methods=['GET', 'POST'])
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
    
    return render_template('create_paper_trades.html')
