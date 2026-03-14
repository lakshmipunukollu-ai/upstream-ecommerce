from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('<uuid:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]
