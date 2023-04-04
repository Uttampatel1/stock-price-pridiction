from flask import Flask, render_template, request
import json
import tiingo

app = Flask(__name__)
config = {
    'session': True,
    'api_key': 'a645fee24b4c7ff5222ad0b26aa9b8819d6788df'
}
client = tiingo.TiingoClient(config)

def get_stock_data(symbol):
    stock_data = client.get_dataframe(symbol, frequency='1Min', startDate='2022-04-01')
    return stock_data.to_json(orient='records')

@app.route('/livechart')
def livechart():
    symbol = request.args.get('symbol', 'AAPL')
    symbol = "AAPL"
    stock_data = json.loads(get_stock_data(symbol))
    return render_template('livechart.html', symbol=symbol, stock_data=stock_data)

if __name__ == '__main__':
    app.run(debug=True)
