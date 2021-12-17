from django.urls import path
from .views import (
    OrderCreateView,
    add_item,
    remove_item,
    OrderDetailView
)
app_name = 'orders'

urlpatterns = [
    path('place-order/', OrderCreateView.as_view(), name='order_create'),
    path('add-item/<int:service_option_id>/', add_item, name='add_item'),
    path(
        'remove-item/<int:service_option_id>/<int:order_item_id>/', remove_item, name='remove_item'
    ),
    path('order-detail/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
]
