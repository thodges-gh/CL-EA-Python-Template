import json
from bridge import Bridge


class Adapter:
    base_url = 'https://min-api.cryptocompare.com/data/price'

    def __init__(self, input):
        self.id = input.get('id', '1')
        self.request_data = input.get('data')
        self.bridge = Bridge()
        self.create_request()

    def create_request(self):
        try:
            params = {
                'fsym': self.request_data.get('from', ''),
                'tsyms': self.request_data.get('to', ''),
            }
            response = self.bridge.request(self.base_url, params)
            data = response.json()
            data['result'] = data[self.request_data['to']]
            self.result_success(data)
        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()

    def result_success(self, data):
        self.result = {
            'jobRunID': self.id,
            'data': data,
            'statusCode': 200,
        }

    def result_error(self, error):
        self.result = {
            'jobRunID': self.id,
            'status': 'errored',
            'error': f'There was an error: {error}',
            'statusCode': 500,
        }
