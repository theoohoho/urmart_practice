from django.db import models


class Customer(models.Model):
    customer_id = models.CharField(max_length=50, primary_key=True)
    customer_name = models.CharField(max_length=100)
    vip = models.BooleanField(default=False)


class Shop(models.Model):
    shop_id = models.CharField(
        max_length=10, primary_key=True)
    shop_name = models.CharField(max_length=100)


class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    stock_pcs = models.IntegerField(default=0, null=False)
    price = models.IntegerField(default=0, null=False)
    shop_id = models.ForeignKey(
        Shop, on_delete=models.CASCADE, db_column='shop_id')
    vip = models.BooleanField(default=False)


class Order(models.Model):
    order_id = models.CharField(
        max_length=100, primary_key=True)
    product_id = models.IntegerField(null=False)
    qty = models.IntegerField(default=0, null=False)
    price = models.IntegerField(default=0, null=False)
    shop_id = models.CharField(max_length=10)
    customer_id = models.CharField(max_length=50)
