from django.contrib import admin
from .models import Stock, Category, Cash, StockHistory, CashHistory
from .forms import StockCreateForm


admin.site.register(Category)
admin.site.register(Cash)
admin.site.register(StockHistory)
admin.site.register(CashHistory)


class StockCreateAdmin(admin.ModelAdmin):
    list_display = ['category', 'item_name', 'quantity', 'unit_purchase_price', 'unit_sale_price']
    form = StockCreateForm
    list_filter = ['category']
    search_fields = ['category', 'item_name']


admin.site.register(Stock, StockCreateAdmin)