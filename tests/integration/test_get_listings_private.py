import unittest
import boto3
import json
import subprocess


class GetListingsPrivateTest(unittest.TestCase):

    def setUp(self) -> None:

        self.dynamodb = boto3.client("dynamodb", endpoint_url="http://localhost.localstack.cloud:4566")

    def create_item(self, template_path):

        request = subprocess.check_output(['node', template_path])
        request = json.loads(request)
        self.dynamodb.put_item(**request)

    def query_items(self, template_path):

        request = subprocess.check_output(['node', template_path])
        request = json.loads(request)
        # Workaround since 'query' wants a boolean, not a string
        request['ExpressionAttributeValues'][':isShared']['BOOL'] = \
            request['ExpressionAttributeValues'][':isShared']['BOOL'] == 'true'
        result = self.dynamodb.query(**request)

        return result

    def test_ok(self):

        # Create item
        self.create_item('tests/resources/put-listing-2.js')

        # Query item
        result = self.query_items('tests/resources/get-listings-private-1.js')

        self.assertEqual(result['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertGreaterEqual(result['Count'], 1)
        self.assertEqual(result['Items'][0]['listingId']['S'], 'cd8513e1-5cf0-4375-accd-71d51a0f83aa')

    def test_query_by_size(self):
        """
        Querying by size should return all items with
        width >= (min_width, min_depth) and depth >= (min_depth, min_width)

        (width and depth order is not important)
        """

        # Create items
        self.create_item('tests/resources/put-listing-3.js')
        self.create_item('tests/resources/put-listing-4.js')

        # Query items
        result = self.query_items('tests/resources/get-listings-private-2.js')

        self.assertEqual(result['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertGreaterEqual(result['Count'], 2)

    def test_query_by_availability(self):
        """
        Querying by availability should return all items with an availability range containing (from_date, to_date)

        If from_date is null, it should return all items with an availability range up to to_date.
        If to_date is null, it should return all items with an availability range from from_date.
        If both are null, it should return all items with any availability range.

        Items that are not any more available should be filtered out by setting to_date to the current date.
        """

        # Create item
        self.create_item('tests/resources/put-listing-5.js')

        # Query items

        result = self.query_items('tests/resources/get-listings-private-3.js')
        self.assertEqual(result['ResponseMetadata']['HTTPStatusCode'], 200)
        # In this case availability.from is too old
        self.assertEqual(result['Count'], 0)

        result = self.query_items('tests/resources/get-listings-private-4.js')
        self.assertEqual(result['ResponseMetadata']['HTTPStatusCode'], 200)
        # In this case availability.to is not enough
        self.assertEqual(result['Count'], 0)

        result = self.query_items('tests/resources/get-listings-private-5.js')
        self.assertEqual(result['ResponseMetadata']['HTTPStatusCode'], 200)
        # In this case from_date is missing so any availability.from is ok
        self.assertGreaterEqual(result['Count'], 1)

        result = self.query_items('tests/resources/get-listings-private-6.js')
        self.assertEqual(result['ResponseMetadata']['HTTPStatusCode'], 200)
        # In this case to_date is missing so any availability.to is ok
        self.assertGreaterEqual(result['Count'], 1)


if __name__ == '__main__':
    unittest.main()
