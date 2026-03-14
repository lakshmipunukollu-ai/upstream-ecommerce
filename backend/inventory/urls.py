from django.urls import path
from . import views

urlpatterns = [
    path('', views.InventoryListView.as_view(), name='inventory_list'),
    path('low-stock/', views.LowStockView.as_view(), name='low_stock'),
    path('<uuid:product_id>/', views.update_stock, name='update_stock'),
]
