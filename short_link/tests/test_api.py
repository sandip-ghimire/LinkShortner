from django.test.testcases import TestCase
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from faker import Faker
import json


class ShortenLinkTest(TestCase):
    long_url = None
    short_url = None

    def setUp(self):
        self.client = APIClient()

    def test_encode_decode(self):
        # order matters
        self.encode_test()
        self.decode_test()

    def test_not_found(self):
        faker = Faker()
        request_data = {
            'url': faker.url()
        }
        resp = self.client.post(reverse('decode_shortlink'), request_data)
        self.assertEqual(resp.status_code, 404)

    def encode_test(self):
        faker = Faker()
        ShortenLinkTest.long_url = faker.url()
        new_data = {
            'url': ShortenLinkTest.long_url
        }
        resp = self.client.post(reverse('encode_shortlink'), new_data)
        ShortenLinkTest.short_url = json.loads(resp.content).get('url')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(ShortenLinkTest.short_url.startswith(settings.PRE_URL))

    def decode_test(self):
        request_data = {
            'url': ShortenLinkTest.short_url
        }
        resp = self.client.post(reverse('decode_shortlink'), request_data)
        long_url = json.loads(resp.content).get('url')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(long_url, ShortenLinkTest.long_url)
