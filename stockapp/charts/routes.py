import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import yfinance as yf
import pandas as pd
import plotly
import plotly.graph_objects as go
from flask import Blueprint, render_template, request
import requests

charts = Blueprint('charts', __name__)

def get_stock_data(ticker, start_date, end_date, period):
    if period:
        data = yf.download(ticker, period=period, interval='1d')
    else:
        data = yf.download(ticker, start=start_date, end=end_date , interval='1d')
    return data

@charts.route('/chart', methods=['GET', 'POST'])
def get_chart():
    chart_data = None
    if request.method == 'POST':
        ticker = request.form['ticker']
        start_date = request.form['start']
        end_date = request.form['end']
        period = request.form['period']
        chart_type = request.form['chart_type']

        if period:
            # Calculate start and end date based on period
            if period == '1mo':
                start_date = datetime.today() - relativedelta(months=1)
            elif period == '3mo':
                start_date = datetime.today() - relativedelta(months=3)
            elif period == '6mo':
                start_date = datetime.today() - relativedelta(months=6)
            elif period == '1y':
                start_date = datetime.today() - relativedelta(years=1)
            elif period == '2y':
                start_date = datetime.today() - relativedelta(years=2)
            elif period == '5y':
                start_date = datetime.today() - relativedelta(years=5)
            end_date = datetime.today()
        else:
            # Convert start and end dates to datetime objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Get stock data
        data = get_stock_data(ticker, start_date, end_date, period)

        # Create chart
        chart_data = {}
        chart_data['title'] = {'text': ticker + ' Stock Price'}
        chart_data['subtitle'] = {'text': 'Period: ' + period if period else start_date.strftime('%m/%d/%Y') + ' - ' + end_date.strftime('%m/%d/%Y')}
        chart_data['yAxis'] = {'title': {'text': 'Price ($)'}}
        chart_data['xAxis'] = {'type': 'datetime'}
        chart_data['legend'] = {'enabled': False}
        chart_data['plotOptions'] = {'series': {'animation': False}}
        chart_data['series'] = [{'name': 'Price', 'data': data['Close'].values.tolist()}]

        if chart_type == 'bar':
            chart_data['chart'] = {'type': 'bar'}
        elif chart_type == 'area':
            chart_data['chart'] = {'type': 'area'}
        elif chart_type == 'candlestick':
             stock_data = data[['Open', 'High', 'Low', 'Close']].reset_index().rename(columns={'Date': 'x'})
    
        chart_data = json.dumps(chart_data)
        # print(chart_data)
        
    return render_template('charts/chart.html', chart_data=chart_data)


#  Demo chart route
@charts.route('/chartdemo', methods=['GET', 'POST'])
def chartdemo():
    return render_template("charts/index.html")
@charts.route('/pipe', methods=["GET", "POST"])
def pipe():
    payload = {}
    headers = {}
    url = "https://demo-live-data.highcharts.com/aapl-ohlcv.json"
    r = requests.get(url, headers=headers, data ={})
    r = r.json()
    return {"res":r}
