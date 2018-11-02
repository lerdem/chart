import datetime
import json
import unittest

from faker import Faker
from django.urls import reverse
from django.test import client

from api.models import RandomData
from api.views import STRPTIME_YMD


class GetDataListTest(unittest.TestCase):

    url = reverse('list')

    def setUp(self):
        self.client = client.Client()
        # prepare data
        faker = Faker()
        data = []
        for i in range(10):
            obj = RandomData(
                created=datetime.datetime.now() - datetime.timedelta(days=i),
                value1=faker.random_int(100, 450),
                value2=faker.random_int(-100, 350),
            )
            data.append(obj)
        RandomData.objects.bulk_create(data)

    @staticmethod
    def byte_response_to_dict(response):
        assert hasattr(response, 'content')
        decoded_byte_content = response.content.decode('utf-8')
        return json.loads(decoded_byte_content)

    def test_details_ok(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        data = self.byte_response_to_dict(response)

        self.assertEqual(len(data['value2']), 10)
        self.assertEqual(len(data['value1']), 10)
        self.assertEqual(len(data['date']), 10)
        self.assertIn('date_range', data.keys())

    def test_details_range_ok(self):
        from_date = datetime.datetime.now() - datetime.timedelta(days=5)
        to_date = datetime.datetime.now()

        params = {
            'from-date': from_date.strftime(STRPTIME_YMD),
            'to-date': to_date.strftime(STRPTIME_YMD)
        }

        response = self.client.get(self.url, data=params)

        self.assertEqual(response.status_code, 200)

        data = self.byte_response_to_dict(response)

        self.assertEqual(len(data['value2']), 6)
        self.assertEqual(len(data['value1']), 6)
        self.assertEqual(len(data['date']), 6)
        self.assertEqual(data['date_range'], [*params.values()])

    def test_invalid_param_values(self):
        params = {
            'from-date': 'lol',
            'to-date': 'kek'
        }

        response = self.client.get(self.url, data=params)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.context['exception'], 'invalid date')

    def test_invalid_only_one_param(self):
        params = {
            'from-date': 'lol',
        }

        response = self.client.get(self.url, data=params)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.context['exception'], 'has to be 2 or 0 keys')
