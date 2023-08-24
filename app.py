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

@app.route('/', methods=['POST', 'GET'])
def chart():
    symbol = ""
    chart_html = ""
    
    if request.method == 'POST':
        symbol = request.form['symbol']

        stock_info = yf.Ticker(symbol)
        historical_data = stock_info.history(period="max")

        if not historical_data.empty:
            data = historical_data
            data['Gap'] = data['Open'] - data['Close'].shift(1)

            chart = go.Figure(data=[go.Candlestick(x=data.index,
                                                    open=data['Open'],
                                                    high=data['High'],
                                                    low=data['Low'],
                                                    close=data['Close'])])
            chart.add_trace(go.Scatter(x=data.index, y=data['Gap'], mode='lines', name='Gap'))
            chart_html = chart.to_html()

    return render_template('index.html', symbol=symbol, chart_html=chart_html)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
