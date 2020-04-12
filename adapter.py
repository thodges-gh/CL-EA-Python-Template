import json
from bridge import Bridge


class Adapter:
    base_url = 'https://min-api.cryptocompare.com/data/price'

    def __init__(self, input):
        self.id = input.get('id', '1')
        self.request_data = input.get('data')
        if self.validate_request_data():
            self.bridge = Bridge()
            self.create_request()
        else:
            self.result_error('No data provided')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    def create_request(self):
        from_param = self.request_data.get('from', '')
        to_param = self.request_data.get('to', '')
        try:
            params = {
                'fsym': from_param,
                'tsyms': to_param,
            }
            response = self.bridge.request(self.base_url, params)
            data = response.json()
            self.result = data[to_param]
            data['result'] = self.result
            self.result_success(data)
        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()

    def result_success(self, data):
        self.result = {
            'jobRunID': self.id,
            'data': data,
            'result': self.result,
            'statusCode': 200,
        }

    def result_error(self, error):
        self.result = {
            'jobRunID': self.id,
            'status': 'errored',
            'error': f'There was an error: {error}',
            'statusCode': 500,
        }
