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
    dividends = stock_info.dividends

    if not dividends.empty:
        ipo_date = dividends.index[0].strftime('%Y-%m-%d')
        if not start_date:
            start_date = ipo_date
    else:
        start_date = "2020-01-01"  # Default start date if IPO date not available

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