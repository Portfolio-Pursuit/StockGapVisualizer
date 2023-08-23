from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_current_price')
def get_current_price():
    symbol = request.args.get('symbol')
    stock_info = yf.Ticker(symbol)
    current_price = stock_info.history(period="1d")["Close"][0]
    return jsonify({"current_price": current_price})

@app.route('/chart', methods=['POST'])
def chart():
    symbol = request.form['symbol']
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    stock_info = yf.Ticker(symbol)
    historical_data = stock_info.history(period="max")

    if historical_data.empty:
        start_date = historical_data.index.min().strftime('%Y-%m-%d')

    data = yf.download(symbol, start=start_date, end=end_date)
    data['Gap'] = data['Open'] - data['Close'].shift(1)

    chart = go.Figure(data=[go.Candlestick(x=data.index,
                                            open=data['Open'],
                                            high=data['High'],
                                            low=data['Low'],
                                            close=data['Close'])])
    chart.add_trace(go.Scatter(x=data.index, y=data['Gap'], mode='lines', name='Gap'))

    return chart.to_html()

if __name__ == '__main__':
    app.run(debug=True)