from .models import OrderItem


def order_item_counter(request):
    item_count = 0
    try:
        item_count = OrderItem.objects.select_related('service').filter(
            user=request.user,
            is_ordered=False
        ).count() if request.user.is_authenticated else 0
    except OrderItem.DoesNotExist:
        item_count = 0

    return {'item_count': item_count}
