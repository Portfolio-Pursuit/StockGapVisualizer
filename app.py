from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

app = Flask(__name__)

@app.route('/landing')
def index():
    return render_template('index.html')

@app.route('/get_current_price')
def get_current_price():
    symbol = request.args.get('symbol')
    stock_info = yf.Ticker(symbol)
    current_price = stock_info.history(period="1d")["Close"][0]
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
            autosize=True,  # Automatically adjust size to container
            margin=dict(l=40, r=20, t=40, b=20),  # Set margin
            xaxis=dict(rangeslider=dict(visible=False))  # Disable range slider
        )
        
        return chart.to_html()
    
    return ""

def check_target_price(current_price, target_price):
    if current_price >= target_price:
        print(f"Target price of ${target_price} reached!\nCurrent price: ${current_price}")
        # You could also send an email or notification here if desired

@app.route('/', methods=['POST', 'GET'])
def chart():
    symbol = ""
    chart_html = ""

    if request.method == 'POST':
        symbol = request.form['symbol']
        target_price = request.form.get('target_price')

        stock_info = yf.Ticker(symbol)
        current_price = stock_info.history(period="1d")["Close"][0]

        if target_price and target_price != "":
            target_price = float(target_price)
            check_target_price(current_price, target_price)

        chart_html = generate_chart(symbol)

    return render_template('index.html', symbol=symbol, chart_html=chart_html)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
