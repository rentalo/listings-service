import unittest
import boto3
import json
import subprocess


class GetUserListingsTest(unittest.TestCase):

    def setUp(self) -> None:

        self.dynamodb = boto3.client("dynamodb", endpoint_url="http://localhost.localstack.cloud:4566")

    def create_item(self, template_path):

        request = subprocess.check_output(['node', template_path])
        request = json.loads(request)
        self.dynamodb.put_item(**request)

    def query_items(self, template_path):

        request = subprocess.check_output(['node', template_path])
        request = json.loads(request)
        result = self.dynamodb.query(**request)

        return result

    def test_query_by_owner(self):
        """
        Querying by owner should return all items created by the given owner
        """

        # Create item
        self.create_item('tests/resources/put-listing-6.js')

        # Query items

        result = self.query_items('tests/resources/get-user-listings-1.js')
        # In this case user has created at least one item
        self.assertEqual(result['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertGreaterEqual(result['Count'], 1)

        result = self.query_items('tests/resources/get-user-listings-2.js')
        # In this case user has created no items
        self.assertEqual(result['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertGreaterEqual(result['Count'], 0)


if __name__ == '__main__':
    unittest.main()
