# Generated by Django 4.1.4 on 2022-12-19 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_stock_purchased_from"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cash",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("recipient", models.CharField(max_length=50)),
                ("detail", models.TextField(max_length=50)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("amount_in", models.DecimalField(decimal_places=2, max_digits=10)),
                ("amount_out", models.DecimalField(decimal_places=2, max_digits=10)),
                ("balance", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]