from django.urls import path
from .views import (
    OrderCreateView,
    add_item,
    remove_item,
)
app_name = 'orders'

urlpatterns = [
    path('place-order/', OrderCreateView.as_view(), name='create_order'),
    path('add-item/<int:service_option_id>/', add_item, name='add_item'),
    path(
        'remove-item/<int:service_option_id>/<int:order_item_id>/', remove_item, name='remove_item'
    ),

]
