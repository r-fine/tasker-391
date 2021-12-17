from django.utils.safestring import mark_safe

import django_tables2 as tables

from .models import Staff
from apps.services.models import Service, ServiceOption
from apps.orders.models import Order


class StaffTable(tables.Table):
    activate = {
        'td': {'data-href': lambda record: record.activation_url}
    }
    editable = {
        'td': {'data-href': lambda record: record.get_absolute_url}
    }
    deletable = {
        'td': {'data-href': lambda record: record.delete_url}
    }
    is_active = tables.Column(
        attrs=activate,
    )
    edit = tables.Column(
        attrs=editable, orderable=False,
        default=mark_safe(
            '<button class="btn btn-sm"><i class="bi bi-pencil-square"></i></button>'
        )
    )
    delete = tables.Column(
        attrs=deletable, orderable=False,
        default=mark_safe(
            '<button class="btn btn-sm"><i class="bi bi-trash"></i></button>'
        )
    )
    full_name = tables.Column(orderable=False)
    department__name = tables.Column(verbose_name='Department')

    class Meta:
        model = Staff
        template_name = 'django_tables2/bootstrap4.html'
        fields = (
            'full_name', 'department__name', 'phone', 'address',
            'is_active', 'edit', 'delete',
        )
        attrs = {
            'class': 'table table-striped table-hover',
            'id': 'myTable',
        }


class ServiceTable(tables.Table):
    editable = {
        'td': {'data-href': lambda record: record.edit_url}
    }
    deletable = {
        'td': {'data-href': lambda record: record.delete_url}
    }
    edit = tables.Column(
        attrs=editable, orderable=False,
        default=mark_safe(
            '<button class="btn btn-sm"><i class="bi bi-pencil-square"></i></button>'
        )
    )
    delete = tables.Column(
        attrs=deletable, orderable=False,
        default=mark_safe(
            '<button class="btn btn-sm"><i class="bi bi-trash"></i></button>'
        )
    )
    is_parent = tables.Column(orderable=False)

    class Meta:
        model = Service
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('name', 'is_parent', 'edit', 'delete',)
        attrs = {
            'class': 'table table-striped table-hover',
            'id': 'myTable',
        }


class ServiceOptionTable(tables.Table):
    editable = {
        'td': {'data-href': lambda record: record.edit_url}
    }
    deletable = {
        'td': {'data-href': lambda record: record.delete_url}
    }
    edit = tables.Column(
        attrs=editable, orderable=False,
        default=mark_safe(
            '<button class="btn btn-sm"><i class="bi bi-pencil-square"></i></button>'
        )
    )
    delete = tables.Column(
        attrs=deletable, orderable=False,
        default=mark_safe(
            '<button class="btn btn-sm"><i class="bi bi-trash"></i></button>'
        )
    )

    class Meta:
        model = ServiceOption
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('service', 'name', 'edit', 'delete',)
        attrs = {
            'class': 'table table-striped table-hover',
            'id': 'myTable',
        }
