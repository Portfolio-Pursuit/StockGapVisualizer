# app.py

from flask import Flask, redirect, Response, render_template, request, jsonify, url_for, session, abort
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from flask_caching import Cache
import plotly.express as px
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 3600})  # Cache for 1 hour

sp500 = pd.read_html(r'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']

@app.route('/landing')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here (e.g., check credentials)
        username = request.form['username']
        password = request.form['password']
        # Example: Check if the username and password are correct
        if username == 'your_username' and password == 'your_password':
            # Store authentication status in the session
            session['authenticated'] = True
            return redirect(url_for('dashboard'))

        # Display an error message for an incorrect login
        error_message = 'Invalid username or password'
        return render_template('login.html', error_message=error_message)

    # If it's a GET request, render the login form
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the authentication status from the session
    session.pop('authenticated', None)
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    # Check if the user is authenticated
    if not session.get('authenticated'):
        return redirect('/login')

    return render_template('dashboard.html')

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

heatmap_data = pd.DataFrame()

@app.route('/heatmap')
def heatmap():
    global heatmap_data
    startIdx = int(request.args.get('startIdx', 0))  # Get the start index from the query parameters
    if (len(heatmap_data) != startIdx):
        startIdx = 0
        heatmap_data = generate_heatmap_data(startIdx=startIdx, useStartIdx=True)
    elif (len(heatmap_data) >= len(sp500)):
        pass
    elif (len(heatmap_data) == 0 or startIdx == 0):
        heatmap_data = generate_heatmap_data(startIdx=startIdx, useStartIdx=True)
    else:
        heatmap_data = pd.concat([heatmap_data, generate_heatmap_data(startIdx=startIdx, useStartIdx=True)], ignore_index=True) 
    heatmap = create_heatmap(heatmap_data)  # Create the heatmap using Plotly

    # Check if there are more items to load
    if (startIdx + 25) < len(sp500):
        # Create a JavaScript timer that calls the `/heatmap` route with the next start index
        script = f'''
            <script>
                setTimeout(function() {{
                    window.location.href = "/heatmap?startIdx={startIdx + 25}";
                }}, 100);  // Adjust the interval (in milliseconds) as needed
            </script>
        '''
    else:
        script = ''

    # Use a Flask Response to send both the heatmap and the JavaScript
    return Response(heatmap + script, content_type='text/html')

def create_heatmap(heatmap_data):
    color_bin = [-1,-0.02,-0.01,0, 0.01, 0.02,1]

    heatmap_data['colors'] = pd.cut(heatmap_data['delta'], bins=color_bin, labels=['red','indianred','lightpink','lightgreen','lime','green'])
        
    trace = px.treemap(heatmap_data, path=[px.Constant("all"), 'sector','ticker'], values = 'market_cap', color='colors',
                 color_discrete_map ={'(?)':'#262931', 'red':'red', 'indianred':'indianred','lightpink':'lightpink', 'lightgreen':'lightgreen','lime':'lime','green':'green'},

                hover_data = {'delta':':.2p'}
                )

    trace.update_layout(
        title="Stock Percent Change Heatmap (Treemap)",
        autosize=False,
        width=1200,
        height=800)
    
    return trace.to_html()

@app.route('/update_heatmap_data')
def update_heatmap_data():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    updated_heatmap_data = generate_heatmap_data(start_date, end_date)
    return jsonify({"heatmap": create_heatmap(updated_heatmap_data)})

def generate_heatmap_data(start_date=None, end_date=None, startIdx=0, useStartIdx=False):
    tickers = []
    sectors = []
    deltas = []
    market_caps = []

    # If start_date or end_date is not provided, default to the last 7 days
    if not start_date:
        start_date = (pd.Timestamp.now() - pd.DateOffset(days=7)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = pd.Timestamp.now().strftime('%Y-%m-%d')

    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')

    period = (end_date_dt - start_date_dt).days

    def process_stock_data(ticker):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            sector = info.get('sector', 'Other')
            
            hist = stock.history(period=f"{period}d", start=start_date, end=end_date)
            if len(hist) >= 2:
                delta = (hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]
            else:
                delta = 0
            
            if 'sharesOutstanding' in info and 'previousClose' in info:
                market_cap = info['sharesOutstanding'] * info['previousClose']
            else:
                market_cap = 0
            
            tickers.append(ticker)
            sectors.append(sector)
            deltas.append(delta)
            market_caps.append(market_cap)
           
            print(f"Downloaded data for {ticker}")
        except Exception as e:
            print(f"Error for {ticker}: {e}")


        return {'ticker': tickers, 'sector': sectors, 'delta': deltas, 'market_cap': market_caps}

    with ThreadPoolExecutor() as executor:
        for result in executor.map(process_stock_data, sp500[startIdx:startIdx+25] if useStartIdx else sp500):
            continue

    data = result
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.transpose()

    return df

if __name__ == '__main__':
    app.run(port=8000, debug=True)

