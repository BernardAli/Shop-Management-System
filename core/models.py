from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    item_description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    purchased_quantity = models.IntegerField(default='0', blank=True, null=True)
    purchased_by = models.CharField(max_length=50, blank=True, null=True)
    purchased_from = models.CharField(max_length=50, blank=True, null=True)
    unit_purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sale_quantity = models.IntegerField(default='0', blank=True, null=True)
    sale_by = models.CharField(max_length=50, blank=True, null=True)
    sale_to = models.CharField(max_length=50, blank=True, null=True)
    unit_sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    export_to_CSV = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name


class StockHistory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    item_description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    purchased_quantity = models.IntegerField(default='0', blank=True, null=True)
    purchased_by = models.CharField(max_length=50, blank=True, null=True)
    purchased_from = models.CharField(max_length=50, blank=True, null=True)
    unit_purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sale_quantity = models.IntegerField(default='0', blank=True, null=True)
    sale_by = models.CharField(max_length=50, blank=True, null=True)
    sale_to = models.CharField(max_length=50, blank=True, null=True)
    unit_sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    expiry = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.item_name


CASH_CHOICE = (
    ('Bank', 'Bank'),
    ('Cash', 'Cash'),
)


class Cash(models.Model):
    category = models.CharField(max_length=50, blank=True, null=True, choices=CASH_CHOICE)
    recipient = models.CharField(max_length=50)
    detail = models.TextField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    amount_in = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_out = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    impriest_level = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    export_to_CSV = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category}"


class CashHistory(models.Model):
    category = models.CharField(max_length=50, blank=True, null=True, choices=CASH_CHOICE)
    recipient = models.CharField(max_length=50, blank=True, null=True)
    detail = models.TextField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    amount_in = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_out = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    impriest_level = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.category}"