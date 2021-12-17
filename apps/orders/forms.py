from django import forms
from django.core.exceptions import ValidationError

from .models import Order, OrderItem
from apps.accounts.models import Staff


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'phone', 'email',
            'address_line_1', 'address_line_2', 'area', 'order_note', 'date', 'time',
        ]


class AdminOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'user', 'order_number', 'first_name', 'last_name', 'phone', 'email',
            'address_line_1', 'address_line_2', 'area', 'order_note', 'date', 'time',
            'is_ordered',
        ]


class AdminOrderItemForm(forms.ModelForm):
    assigned_staff = forms.ModelChoiceField(
        queryset=Staff.objects.all().filter(is_active=True),
        required=False
    )

    class Meta:
        model = OrderItem
        fields = [
            'service', 'assigned_staff', 'status', 'is_reviewable'
        ]
