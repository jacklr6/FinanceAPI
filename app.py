from flask import Flask, request, jsonify
import yfinance as yf
from datetime import datetime
import time
import pytz
import pandas_market_calendars as mcal

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
            'longName': info.get('longName'),
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
            'beta': info.get('beta'),
            'profitMargins': info.get('profitMargins'),
            'returnOnEquity': info.get('returnOnEquity'),
            'grossMargins': info.get('grossMargins'),
            'operatingMargins': info.get('operatingMargins'),
            'currency': info.get('currency'),
            'exchange': info.get('exchange'),
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'longBusinessSummary': info.get('longBusinessSummary'),
            'website': info.get('website'),
            'address1': info.get('address1'),
            'city': info.get('city'),
            'state': info.get('state'),
            'zip': info.get('zip'),
            'country': info.get('country'),
            'timestamp': info.get('regularMarketTime'),
            'last_close_from_history': last_close,
            'market_open': is_market_open()
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_stock_history():
    symbol = request.args.get('symbol')
    period = request.args.get('period', default='5d')       # default: 5 days
    interval = request.args.get('interval', default='1h')   # default: 1 hour

    if not symbol:
        return jsonify({'error': 'Missing symbol parameter'}), 400

    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)

        if hist.empty:
            return jsonify({'error': 'No historical data available'}), 404

        history_data = []
        for index, row in hist.iterrows():
            history_data.append({
                'timestamp': int(index.timestamp()),
                'price': row['Close']
            })

        return jsonify({
            'symbol': symbol.upper(),
            'period': period,
            'interval': interval,
            'data': history_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def is_market_open():
    nyse = mcal.get_calendar('NYSE')
    eastern = pytz.timezone('US/Eastern')
    now = datetime.now(eastern)

    schedule = nyse.schedule(start_date=now.date(), end_date=now.date())
    if schedule.empty:
        return False  # holiday/weekend

    market_open = schedule.iloc[0]['market_open'].tz_convert(eastern)
    market_close = schedule.iloc[0]['market_close'].tz_convert(eastern)

    return market_open <= now <= market_close
