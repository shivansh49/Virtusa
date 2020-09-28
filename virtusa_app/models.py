from django.db import models

class product(models.Model):
    product_name = models.CharField(max_length=200)
    product_desc = models.CharField(max_length=200)
    product_price = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200)
class products(models.Model):
    product_name = models.CharField(max_length=200)
    product_desc = models.CharField(max_length=200)
    product_price = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200)
class product3(models.Model):
    product_name = models.CharField(max_length=200)
    product_desc = models.CharField(max_length=200)
    product_price = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200)