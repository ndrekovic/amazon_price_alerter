# Create your models here.
from django.db import models


class Product(models.Model):
    asin = models.CharField(max_length=10, unique=True, db_index=True, blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)  # <-- nur URL
    title = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)  # , on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    desired_price = models.DecimalField(max_digits=8, decimal_places=2)
    mail_has_been_sent = models.BooleanField(default=False)


    @staticmethod
    def print_instance_attributes():
        attributes = []
        for attribute in Product.__dict__.keys():
            if (not attribute.startswith('_')) and (attribute != 'id'):
                attributes.append(attribute)
        return attributes
