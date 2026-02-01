#!/usr/bin/env python3

import logging
import os

from django.core.management.base import BaseCommand

from products.emails import send_price_alert
from products.models import Product
from products.utils import scrape_amazon_price_alerter


# configure django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "amazon_price_alerter.settings")

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Update product prices and send alerts"


    def handle(self, *args, **kwargs):
        logger.info("Price update started")

        products = Product.objects.all()
        if not products.exists():
            logger.info("No products found")
            return

        for product in products:
            try:
                data = scrape_amazon_price_alerter(product.url)
                if not data:
                    continue
                new_price = data["price"]

                # update old price of product
                product.price = new_price
                product.save()

                if new_price <= product.desired_price and not product.mail_has_been_sent:
                    send_price_alert(product.url, new_price, product.desired_price)

                    # prevent email from being sent multiple times
                    product.mail_has_been_sent = True
                    product.save()

            except Exception as e:
                logger.error(f"Error for product {product.id}: {e}")

        logger.info("Price update finished")
