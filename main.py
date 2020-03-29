import json
from bridge import Bridge


def create_request(input):
    bridge = Bridge()
    try:
        params = {
            'fsym': input['data']['from'],
            'tsyms': input['data']['to']
        }
        response = bridge.request(
            'https://min-api.cryptocompare.com/data/price', params)
        data = response.json()
        data['result'] = data[input['data']['to']]
        return {
            'jobRunID': input['id'],
            'data': data,
            'statusCode': 200
        }
    except Exception as e:
        return adapter_error(input['id'], f'There was an error: {e}')
    finally:
        bridge.close()


def adapter_error(job_run_id, error):
    return {
        'jobRunID': job_run_id,
        'status': 'errored',
        'error': error,
        'statusCode': 500
    }


def lambda_handler(event, context):
    result = create_request(event)
    return result


def gcs_handler(request):
    cl_data = request.json
    result = create_request(cl_data)
    return json.dumps(result)
