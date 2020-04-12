from bridge import Bridge


class Adapter:
    base_url = 'https://min-api.cryptocompare.com/data/price'
    from_params = ['base', 'from', 'coin']
    to_params = ['quote', 'to', 'market']

    def __init__(self, input):
        self.id = input.get('id', '1')
        self.request_data = input.get('data')
        if self.validate_request_data():
            self.bridge = Bridge()
            self.set_params()
            self.create_request()
        else:
            self.result_error('No data provided')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    def set_params(self):
        for param in self.from_params:
            self.from_param = self.request_data.get(param)
            if self.from_param is not None:
                break
        for param in self.to_params:
            self.to_param = self.request_data.get(param)
            if self.to_param is not None:
                break

    def create_request(self):
        try:
            params = {
                'fsym': self.from_param,
                'tsyms': self.to_param,
            }
            response = self.bridge.request(self.base_url, params)
            data = response.json()
            self.result = data[self.to_param]
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
