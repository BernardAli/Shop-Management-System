# Generated by Django 4.1.4 on 2022-12-19 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_rename_purchase_price_stock_unit_purchase_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="stock",
            name="total_purchase_price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="stock",
            name="total_sale_price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
