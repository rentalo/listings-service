import unittest
import subprocess
import json


class GetListingsResponseTest(unittest.TestCase):

    def test_ok(self):

        response = subprocess.check_output(['node', 'tests/resources/get-listings-response-1.js'])
        response = json.loads(response)

        self.assertEqual(len(response['listings']), 1)
        self.assertEqual(response['listings'][0]['photos'][0], 'avMQpjqbGEzCCPuTZjTEJQ==')
        self.assertEqual(response['listings'][0]['photos'][1], 'bvMQpjqbGEzCCPuTZjTEJQ==')
        self.assertEqual(response['listings'][0]['address']['street'], 'Via Roma 123')
        self.assertEqual(response['listings'][0]['address']['city'], 'Torino')
        self.assertEqual(response['listings'][0]['address']['state'], 'TO')
        self.assertEqual(response['listings'][0]['address']['zip'], '12345')
        self.assertEqual(response['listings'][0]['address']['country'], 'Italy')


if __name__ == '__main__':
    unittest.main()
