from django.dispatch import receiver
from django.contrib.auth.models import Group

from allauth.account.signals import user_logged_in, user_signed_up

from .models import Staff


@receiver(user_logged_in)
def staff_profile(request, user, **kwargs):
    if user.is_superuser == False and user.is_staff:
        if not Staff.objects.filter(user=user).exists():
            group = Group.objects.get_or_create(name='STAFF')
            group[0].user_set.add(user)
            Staff.objects.create(user=user)


@receiver(user_signed_up)
def group_customer(request, user, **kwargs):
    if user.is_staff == False:
        group = Group.objects.get_or_create(name='CUSTOMER')
        group[0].user_set.add(user)


@receiver(user_logged_in)
def group_admin(request, user, **kwargs):
    if user.is_superuser:
        group = Group.objects.get_or_create(name='ADMIN')
        group[0].user_set.add(user)
