# heatmap.py
from flask import Blueprint, Response, request, jsonify
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from common.auth.login_required import login_required
import plotly.express as px
import yfinance as yf

heatmap_blueprint = Blueprint('heatmap', __name__)

sp500 = pd.read_html(r'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']

heatmap_data = pd.DataFrame()

@heatmap_blueprint.route('/')
@login_required
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

@heatmap_blueprint.route('/update_heatmap_data')
@login_required
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