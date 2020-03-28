# coding: utf-8
from flask import Flask, request, jsonify

import main as external_adapter

app = Flask(__name__)


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


@app.route('/', methods=['POST'])
def call_adapter():
    test_data = request.get_json()
    if test_data == '':
        test_data = {}
    result = external_adapter.create_request(test_data)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080', threaded=True)
