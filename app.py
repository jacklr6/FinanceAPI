from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/price', methods=['GET'])
def get_stock_price():
    symbol = request.args.get('symbol')

    if not symbol:
        return jsonify({'error': 'Missing symbol parameter'}), 400

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        data = {
            'symbol': symbol.upper(),
            'current_price': info.get('regularMarketPrice'),
            'daily_high': info.get('dayHigh'),
            'daily_low': info.get('dayLow'),
            'pe_ratio': info.get('trailingPE'),
            'timestamp': info.get('regularMarketTime')
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500