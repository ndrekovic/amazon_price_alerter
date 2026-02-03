from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from products.models import Product
from ..views import parse_price


class AddProductTests(TestCase):

    @patch("products.views.parse_price")
    def test_add_product_not_existing(self, mock_scrape):
        mock_scrape.return_value = {
            "title": "Test Produkt",
            "price": 99.99,
            "image_url": "http://img.test",
            "url": "http://amazon.test"
        }

        response = self.client.post("/add_product/", {
            "amzn_url": "http://amazon.test",
            "desired_price": "150"
        })

        data = response.json()

        self.assertEqual(data["status"], "not_existing")

    def test_add_product_empty_url(self):
        response = self.client.post(
            reverse("add_prod"),
            {
                "amzn_url": "",
                "desired_price": "20.00"
            }
        )

        data = response.json()
        self.assertEqual(data["status"], "empty_url_field")

        self.assertEqual(Product.objects.count(), 0)

    def test_add_product_invalid_url(self):
        url = "https://www.amzzqwewqeon.de/dp/B0CHXFCYCR/ref=twister_B0CJ2N73DK?_encoding=UTF8&th=1"
        response = self.client.post(
            reverse("add_prod"),
            {
                "amzn_url": url,
                "desired_price": "20.00"
            }
        )

        data = response.json()
        self.assertEqual(data["status"], "not_existing")

        self.assertEqual(Product.objects.count(), 0)

    def test_add_product_empty_price(self):
        response = self.client.post(
            reverse("add_prod"),
            {
                "amzn_url": "https://amazon.de/dp/B012345678",
                "desired_price": ""
            }
        )

        self.assertEqual(response.json()["status"], "only_numbers")

class DeleteProductTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            asin="B012345678",
            url="https://amazon.de/dp/B012345678",
            desired_price=20,
            price=30,
            title="Test",
            image_url=""
        )

    def test_delete_product(self):
        response = self.client.post(
            reverse("delete_prod"),
            {
                "asin": self.product.asin
            }
        )

        self.assertEqual(response.json()["status"], "deleted")
        self.assertEqual(Product.objects.count(), 0)

class PriceParserTests(TestCase):

    def test_valid_price(self):
        self.assertEqual(parse_price("10"), Decimal("10.00"))
        self.assertEqual(parse_price("10,5"), Decimal("10.50"))
        self.assertEqual(parse_price("601.77777"), Decimal("601.77"))
        self.assertEqual(parse_price("10,995"), Decimal("10.99"))

    def test_invalid_price(self):
        self.assertIsNone(parse_price("abc"))
        self.assertIsNone(parse_price("10a"))
        self.assertIsNone(parse_price(""))
        self.assertIsNone(parse_price("-5"))
        self.assertIsNone(parse_price("10.0.0.0"))
        self.assertIsNone(parse_price("10,03,3"))
