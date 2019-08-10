#!/usr/bin/env python3
import os
from functools import wraps
from flask import Flask, jsonify
from alpha_vantage.timeseries import TimeSeries

ts = None
init_error = None
application = Flask(__name__)

try:
    alpha_vantage_api_key_filename = os.environ['ALPHA_VANTAGE_API_KEY_FILE']
    alpha_vantage_api_key = open(alpha_vantage_api_key_filename, 'r').read()
    ts = TimeSeries(key=alpha_vantage_api_key)
    if ts is None:
        raise RuntimeError('Failed to create TimeSeries object')
except Exception as e:
    init_error = str(e)

@application.route("/api/v1/stock/<symbol>")
def stock(symbol):
    try:
        if init_error:
            return jsonify(error=init_error), 500

        data, meta_data = ts.get_intraday(symbol)
        last_refresh = meta_data['3. Last Refreshed']
        last_data = data[last_refresh]
        closing_price = last_data['4. close']

        return jsonify(
            closing_price=closing_price
        )
    except Exception as e:
        return jsonify(error = str(e)), 500

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80)
