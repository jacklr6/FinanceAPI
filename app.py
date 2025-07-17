from flask import Flask, jsonify, request
import yfinance as yf

app = Flask(__name__)

@app.route('/price')
def get_price():
    symbol = request.args.get('symbol', default='AAPL')
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        latest = data.iloc[-1]
        return jsonify({
            'symbol': symbol,
            'price': latest['Close'],
            'open': latest['Open'],
            'high': latest['High'],
            'low': latest['Low'],
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)