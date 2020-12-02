def test_call_adapter(client):
    assert client.post('/').status_code == 500
    assert client.get('/').status_code == 405

    rv = client.post('/', json={'id': '1', 'data': {}})
    json_data = rv.get_json()
    assert json_data.get('statusCode') == 500
    assert json_data.get('status') == 'errored'
