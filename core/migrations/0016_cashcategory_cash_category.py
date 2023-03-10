# Generated by Django 4.1.4 on 2022-12-20 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0015_stockhistory"),
    ]

    operations = [
        migrations.CreateModel(
            name="CashCategory",
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
                    "name",
                    models.CharField(
                        blank=True,
                        choices=[("Bank", "Bank"), ("Cash", "Cash")],
                        max_length=50,
                        null=True,
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name="cash",
            name="category",
            field=models.ForeignKey(
                blank=True,
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.cashcategory",
            ),
            preserve_default=False,
        ),
    ]
