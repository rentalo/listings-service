import unittest
import boto3
import json
import subprocess


class PutListingTest(unittest.TestCase):

    def setUp(self) -> None:

        self.dynamodb = boto3.client("dynamodb", endpoint_url="http://localhost.localstack.cloud:4566")

    def test_ok(self):

        request = subprocess.check_output(['node', 'tests/resources/put-listing-1.js'])
        request = json.loads(request)
        result = self.dynamodb.put_item(**request)
        self.assertEqual(result['ResponseMetadata']['HTTPStatusCode'], 200)


if __name__ == '__main__':
    unittest.main()
