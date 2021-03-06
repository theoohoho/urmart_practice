# Generated by Django 3.1.7 on 2021-02-22 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=100)),
                ('vip', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('product_id', models.IntegerField()),
                ('qty', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('shop_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('shop_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('shop_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.IntegerField(primary_key=True, serialize=False)),
                ('stock_pcs', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('vip', models.BooleanField(default=False)),
                ('shop_id', models.ForeignKey(db_column='shop_id', on_delete=django.db.models.deletion.CASCADE, to='dashboard.shop')),
            ],
        ),
    ]
