# Generated by Django 4.1.4 on 2022-12-20 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_cashhistory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cashhistory",
            name="detail",
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="cashhistory",
            name="recipient",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
