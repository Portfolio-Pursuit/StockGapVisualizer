# chart.chart.py
from flask import Blueprint, render_template, request, jsonify, url_for
import yfinance as yf
import plotly.graph_objs as go
from common.auth.login_required import login_required
from common.ui.navbar import navbar, getUIDir

renderEnv = navbar(getUIDir(__file__)).getEnv()

chart_blueprint = Blueprint('chart', __name__, static_folder='static', static_url_path='assets')
local_template = 'chart.html'

@chart_blueprint.route('/', methods=['POST', 'GET'])
@login_required
def chart():
    symbol = ""
    chart_html = ""
    current_price = 50

    if request.method == 'POST':
        symbol = request.form['symbol']
        target_price = request.form.get('target_price')

        stock_info = yf.Ticker(symbol)
        current_price = stock_info.history(period="1d")["Close"][0]

        if target_price and target_price != "":
            target_price = float(target_price)
            check_target_price(current_price, target_price)

        chart_html = generate_chart(symbol)
    else:
        symbol = 'SPY'
        stock_info = yf.Ticker(symbol)
        current_price = stock_info.history(period="1d")["Close"][0]
        target_price = current_price

        if target_price and target_price != "":
            target_price = float(target_price)
            check_target_price(current_price, target_price)

        chart_html = generate_chart(symbol)

    return renderEnv.get_template(local_template).render(symbol=symbol, chart_html=chart_html, current_price=current_price)

@chart_blueprint.route('/get_current_price')
@login_required
def get_current_price():
    symbol = request.args.get('symbol')
    stock_info = yf.Ticker(symbol)
    try:
        current_price = stock_info.history(period="1d")["Close"][0]
        current_price = round(current_price, 2)
    except:
        current_price = 'Unknown'
    return jsonify({"current_price": current_price})

def generate_chart(symbol):
    stock_info = yf.Ticker(symbol)
    data = stock_info.history(period="max")
    
    if not data.empty:
        data['Gap'] = data['Open'] - data['Close'].shift(1)
        
        chart = go.Figure(data=[go.Candlestick(x=data.index,
                                                open=data['Open'],
                                                high=data['High'],
                                                low=data['Low'],
                                                close=data['Close'])])
        chart.add_trace(go.Scatter(x=data.index, y=data['Gap'], mode='lines', name='Gap'))
        
        chart.update_layout(
            autosize=True,
            margin=dict(l=40, r=20, t=40, b=20),
            xaxis_rangeslider_visible=True
        )
        
        return chart.to_html()
    
    return ""

def check_target_price(current_price, target_price):
    if current_price >= target_price:
        print(f"Target price of ${target_price} reached!\nCurrent price: ${current_price}")
        # You could also send an email or notification here if desired
