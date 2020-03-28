import unittest
import main as adapter


class TestAdapter(unittest.TestCase):

    def test_request(self):
        job_run_id = '278c97ffadb54a5bbb93cfec5f7b5503'
        test_data = {
            'id': job_run_id,
            'data': {
                'from': 'ETH',
                'to': 'USD'
            }
        }
        result = adapter.create_request(test_data)
        self.assertEqual(200, result['statusCode'])
        self.assertEqual(job_run_id, result['jobRunID'])
        self.assertIsNotNone(result['data'])
        self.assertIsInstance(result['data']['result'], float)

    def test_params_not_specified(self):
        job_run_id = '278c97ffadb54a5bbb93cfec5f7b5503'
        test_data = {
            'id': job_run_id,
            'data': {}
        }
        result = adapter.create_request(test_data)
        self.assertEqual(500, result['statusCode'])
        self.assertEqual(job_run_id, result['jobRunID'])
        self.assertEqual('errored', result['status'])
        self.assertIsNotNone(result['error'])

    def test_bad_params(self):
        job_run_id = '278c97ffadb54a5bbb93cfec5f7b5503'
        test_data = {
            'id': job_run_id,
            'data': {
                'from': 'does_not_exist',
                'to': 'USD'
            }
        }
        result = adapter.create_request(test_data)
        self.assertEqual(500, result['statusCode'])
        self.assertEqual(job_run_id, result['jobRunID'])
        self.assertEqual('errored', result['status'])
        self.assertIsNotNone(result['error'])


if __name__ == '__main__':
    unittest.main()
