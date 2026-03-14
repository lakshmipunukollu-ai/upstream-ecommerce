from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_cart, name='cart'),
    path('items/', views.add_item, name='cart_add_item'),
    path('items/<uuid:item_id>/', views.update_item, name='cart_update_item'),
    path('items/<uuid:item_id>/delete/', views.remove_item, name='cart_remove_item'),
    path('clear/', views.clear_cart, name='cart_clear'),
]
