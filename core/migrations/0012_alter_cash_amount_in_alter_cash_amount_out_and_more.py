# Generated by Django 4.1.4 on 2022-12-19 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_cash_last_updated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cash",
            name="amount_in",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="cash",
            name="amount_out",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="cash",
            name="balance",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
