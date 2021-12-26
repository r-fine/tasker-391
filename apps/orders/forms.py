from django import forms
from django.core.exceptions import ValidationError
# from django.forms.models import inlineformset_factory

from .models import Order, OrderItem
from apps.accounts.models import Staff, StaffBookedDateTime


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


# OrderUpdateFormSet = inlineformset_factory(Order, OrderItem, fields=(
#     'user', 'service', 'assigned_staff', 'status', 'is_reviewable'), extra=0, can_delete=True)


class AdminOrderItemForm(forms.ModelForm):
    assigned_staff = forms.ModelChoiceField(
        queryset=Staff.objects.select_related('user', 'department').all().filter(
            is_active=True,
        ),
        required=False
    )

    class Meta:
        model = OrderItem
        fields = [
            'service', 'assigned_staff', 'status', 'is_reviewable'
        ]

    def clean(self):
        cleaned_data = super().clean()

        staff = cleaned_data.get('assigned_staff')
        obj = StaffBookedDateTime.objects.filter(
            staff=staff, order=self.instance.order, order_item=self.instance
        )
        if obj.exists():
            for o in obj:
                o.delete()

        time = None
        try:
            booked = StaffBookedDateTime.objects.get(
                staff=staff, date=self.instance.order.date,
            )
            time = booked.time
        except StaffBookedDateTime.DoesNotExist:
            booked = None

        if self.instance.order.time == time:
            if self.instance.order == booked.order:
                pass
            else:
                raise ValidationError(
                    'The staff you are trying to assign is already booked on the same slot as the order delivery slot. Try changing the order delivery slot or assign another staff.')

        if staff.department != self.instance.service.service:
            raise ValidationError(
                'Assign staff from the same department as ordered service.')
