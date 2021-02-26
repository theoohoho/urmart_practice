# Generated by Django 3.1.7 on 2021-02-24 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_order_customer_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analytic',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('shop_id', models.CharField(max_length=10)),
                ('total_sales_amount', models.IntegerField(default=0)),
                ('total_sales_products', models.IntegerField(default=0)),
                ('total_orders', models.IntegerField(default=0)),
                ('batch', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]