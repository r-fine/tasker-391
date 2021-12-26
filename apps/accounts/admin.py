from django.contrib import admin
from django import forms
from django.db.models.fields.related import ManyToManyField

from .models import *


@admin.register(LocalUser)
class LocalUserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'is_staff', 'get_group']
    list_filter = ['is_active', 'is_staff']
    list_per_page = 25

    def get_group(self, obj):
        try:
            return obj.groups.values_list('name', flat=True).get()
        except obj.DoesNotExist:
            return 'n/a'

    get_group.short_description = 'Group'


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'phone', 'id', 'is_active']
    exclude = ['booked_on']
    list_editable = ['is_active']
    list_filter = ['is_active']
    list_per_page = 25


@admin.register(StaffBookedDateTime)
class StaffBookedDateTimeAdmin(admin.ModelAdmin):
    list_display = ['staff', 'order', 'order_item', 'date', 'time', 'id']
