# Generated by Django 4.1.4 on 2022-12-20 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_rename_bank_balance_cash_balance_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CashHistory",
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
                (
                    "category",
                    models.CharField(
                        blank=True,
                        choices=[("Bank", "Bank"), ("Cash", "Cash")],
                        max_length=50,
                        null=True,
                    ),
                ),
                ("recipient", models.CharField(max_length=50)),
                ("detail", models.TextField(max_length=50)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "amount_in",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "amount_out",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "impriest_level",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "balance",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("issue_by", models.CharField(blank=True, max_length=50, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
