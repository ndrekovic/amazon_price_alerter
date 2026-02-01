from bs4 import BeautifulSoup
from django.test import TestCase

from ..utils import extract_asin, extract_price


class UtilsTests(TestCase):

    def test_extract_asin(self):
        self.assertEqual(extract_asin("https://www.amazon.de/dp/B0CHXFCYCR/ref=twister_B0CJ2N73DK?_encoding=UTF8&th=1"),
                         "B0CHXFCYCR")

    def test_extract_price(self):
        html = '<span class="a-price-whole">19</span><span class="a-price-fraction">99</span>'
        soup = BeautifulSoup(html, 'html.parser')

        self.assertEqual(extract_price(soup), 19)
