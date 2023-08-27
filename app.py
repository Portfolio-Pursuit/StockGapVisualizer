# app.py

from flask import Flask, render_template, request, jsonify
import yfinance as yf
from yfinance import tickers
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

@app.route('/')
def splash():
    return render_template('splash.html')

@app.route('/chart', methods=['POST', 'GET'])
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

    return render_template('index.html', symbol=symbol, chart_html=chart_html, current_price=current_price)

@app.route('/get_heatmap_data')
def get_heatmap_data():
    heatmap_data = generate_heatmap_data()
    return jsonify(heatmap_data)

@app.route('/update_heatmap_data')
def update_heatmap_data():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    updated_heatmap_data = generate_heatmap_data(start_date, end_date)
    return jsonify(updated_heatmap_data)

def generate_heatmap_data(start_date=None, end_date=None):
    # If start_date or end_date is not provided, default to the last 7 days
    if not start_date:
        start_date = (pd.Timestamp.now() - pd.DateOffset(days=7)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = pd.Timestamp.now().strftime('%Y-%m-%d')

    # Get the list of most active stocks over the last 7 days
    most_active_stocks = get_most_active_stocks(start_date, end_date, num_stocks=200)
    # Generate heatmap data for each sector
    heatmap_data = []
    for sector in set(most_active_stocks['Sector']):
        sector_stocks = most_active_stocks[most_active_stocks['Sector'] == sector]
        sector_heatmap = {
            "sector": sector,
            "stocks": []
        }
        for _, stock in sector_stocks.iterrows():
            sector_heatmap["stocks"].append({
                "symbol": stock["Symbol"],
                "percent_change": get_percent_change(stock["Symbol"], start_date, end_date)
            })
        heatmap_data.append(sector_heatmap)
    print(heatmap_data)
    return heatmap_data

# List of popular stock tickers
popular_tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "FB", "NVDA", "AAPL", "JPM", "JNJ",
    "V", "MA", "UNH", "PG", "HD", "DIS", "BAC", "PYPL", "ADBE", "VZ", "CRM",
    "TSM", "NFLX", "CMCSA", "PEP", "KO", "INTC", "CSCO", "ABBV", "XOM", "MRK",
    "CVX", "WMT", "ABT", "NVDA", "PFE", "GOOG", "TMUS", "WFC", "BMY", "BA",
    "ORCL", "ACN", "COST", "AVGO", "TXN", "AMGN", "NKE", "NEE", "LIN", "DHR",
    "HON", "PM", "QCOM", "UNP", "TM", "MMM", "GE", "SBUX", "NOW", "TMO", "IBM",
    "LOW", "C", "VZ", "INTU", "BA", "CAT", "T", "DIS", "MCD", "LMT", "BUD",
    "JPM", "AMT", "MO", "ABT", "UPS", "USB", "AMD", "MS", "ATVI", "ADP", "DHR",
    "TXN", "PNC", "PLD", "TGT", "BLK", "MDT", "AAPL", "MSFT", "GOOGL", "SPY"
]

def get_most_active_stocks(start_date=None, end_date=None, num_stocks=100):
    stock_data = []
    for ticker in popular_tickers:
        try:
            stock = yf.Ticker(ticker)
            stock_info = stock.info
            if "volume" in stock_info and stock_info["volume"] is not None:
                stock_data.append({
                    "Symbol": ticker,
                    "Sector": stock_info.get("sector", "Unknown"),  # Get sector information or use "Unknown"
                    "Volume": stock_info["volume"]
                })
        except Exception as e:
            print("Error for", ticker, e)

    most_active_stocks = pd.DataFrame(stock_data)
    print(most_active_stocks)
    return most_active_stocks


def get_percent_change(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    historical_data = stock.history(period="1d", start=start_date, end=end_date)
    if not historical_data.empty:
        start_price = historical_data["Close"][0]
        end_price = historical_data["Close"][-1]
        percent_change = ((end_price - start_price) / start_price) * 100
        return percent_change
    return 0.0

if __name__ == '__main__':
    app.run(port=8000, debug=True)
