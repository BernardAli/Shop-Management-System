# Generated by Django 4.1.4 on 2022-12-19 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_stock_total_purchase_price_stock_total_sale_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="stock",
            name="purchased_from",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
