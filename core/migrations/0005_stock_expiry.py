# Generated by Django 4.1.4 on 2022-12-19 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_alter_category_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="stock",
            name="expiry",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
