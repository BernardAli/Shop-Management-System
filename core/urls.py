from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name='home'),
    path('list_items/', views.list_item, name='list_items'),
    path('add_items/', views.add_items, name='add_items'),
    path('update_items/<str:pk>/', views.update_items, name="update_items"),
    path('delete_items/<str:pk>/', views.delete_items, name="delete_items"),
    path('stock_detail/<str:pk>/', views.stock_detail, name="stock_detail"),
    path('reorder_level/<str:pk>/', views.reorder_level, name="reorder_level"),
    path('issue_items/<str:pk>/', views.issue_items, name="issue_items"),
    path('receive_items/<str:pk>/', views.receive_items, name="receive_items"),
    path('cash_items/', views.cash_item, name='cash_item'),
    path('issue_cash/<str:pk>/', views.issue_cash, name="issue_cash"),
    path('received_cash/<str:pk>/', views.receive_cash, name="received_cash"),
]