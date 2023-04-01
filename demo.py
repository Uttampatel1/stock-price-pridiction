import yfinance as yf
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template, request
import json

app = Flask(__name__)

def get_stock_data(ticker, start_date, end_date, period):
    if period:
        data = yf.download(ticker, period=period)
    else:
        data = yf.download(ticker, start=start_date, end=end_date)
    return data


@app.route('/chart', methods=['GET', 'POST'])
def chart():
    chart_data = None
    if request.method == 'POST':
        ticker = request.form['ticker']
        start_date = request.form['start']
        end_date = request.form['end']
        period = request.form['period']

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
        chart_data['yAxis'] = {'title': {'text': 'Price'}}
        chart_data['xAxis'] = {'type': 'datetime'}
        chart_data['legend'] = {'enabled': False}
        chart_data['plotOptions'] = {'series': {'animation': False}}
        chart_data['series'] = [{'name': 'Price', 'data': data['Close'].values.tolist()}]
        chart_data = json.dumps(chart_data)

    return render_template('chart.html', chart_data=chart_data)



if __name__ == '__main__':
    app.run(debug=True)