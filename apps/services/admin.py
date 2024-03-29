from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .models import *


@admin.register(Service)
class ServiceAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count'
                    )
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Service.objects.add_related_count(
            qs,
            ServiceOption,
            'service',
            'products_cumulative_count',
            cumulative=True
        )

        # Add non cumulative product count
        qs = Service.objects.add_related_count(
            qs,
            ServiceOption,
            'service',
            'products_count',
            cumulative=False
        )
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific service)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


admin.site.register(ServiceOption)


@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['subject', 'created_at', 'updated_at']
