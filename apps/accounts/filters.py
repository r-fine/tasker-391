import django_filters

from .models import Staff
# from apps.services.models import Service


class StaffFilter(django_filters.FilterSet):
    # department = django_filters.ModelChoiceFilter(
    #     queryset=Service.objects.filter(level=1)
    # )

    class Meta:
        model = Staff
        fields = ['department']
