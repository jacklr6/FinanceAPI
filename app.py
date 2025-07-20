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

        # Historical data (last 1 day)
        hist = ticker.history(period='1d')
        last_close = hist['Close'].iloc[-1] if not hist.empty else None

        # Expanded data
        data = {
            'symbol': symbol.upper(),
            'current_price': info.get('regularMarketPrice'),
            'previous_close': info.get('previousClose'),
            'open': info.get('open'),
            'daily_high': info.get('dayHigh'),
            'daily_low': info.get('dayLow'),
            'volume': info.get('volume'),
            'market_cap': info.get('marketCap'),
            'pe_ratio': info.get('trailingPE'),
            'eps': info.get('trailingEps'),
            'dividend_yield': info.get('dividendYield'),
            '52_week_high': info.get('fiftyTwoWeekHigh'),
            '52_week_low': info.get('fiftyTwoWeekLow'),
            'currency': info.get('currency'),
            'exchange': info.get('exchange'),
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'website': info.get('website'),
            'timestamp': info.get('regularMarketTime'),
            'last_close_from_history': last_close
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
