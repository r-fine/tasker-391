from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from apps.services.models import Service


class LocalUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name='E-mail Address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Staff(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, verbose_name='ID')
    department = models.ForeignKey(
        Service,
        related_name='department',
        on_delete=models.CASCADE,
        null=True
    )
    user = models.OneToOneField(LocalUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        verbose_name='Profile Picture',
        upload_to="images/",
        default="images/500_500.png"
    )
    phone = models.CharField(verbose_name='Phone Number', max_length=11)
    address = models.TextField(max_length=255, blank=False)
    booked_on = models.ManyToManyField(
        "StaffBookedDateTime", related_name='booked_on'
    )
    is_active = models.BooleanField(
        verbose_name='Active status', default=False
    )

    @property
    def full_name(self):
        return self.user.first_name + " " + self.user.last_name

    def get_user_id(self):
        return self.user.id

    def get_absolute_url(self):
        return reverse('accounts:staff_form', args=[self.pk])

    def delete_url(self):
        return reverse('accounts:staff_delete', args=[self.pk])

    def activation_url(self):
        return reverse('accounts:staff_activate', args=[self.pk])

    def schedule_table_url(self):
        return reverse('accounts:staff_schedule_single', args=[self.pk])

    def __str__(self):
        if self.department == None:
            return self.full_name
        return f'{self.full_name} ({self.department.name})'


class StaffBookedDateTime(models.Model):
    HOURS = (
        ('9:00 a.m.', '9:00 a.m.'), ('10:00 a.m.',
                                     '10:00 a.m.'), ('11:00 a.m.', '11:00 a.m.'),
        ('12:00 p.m.', '12:00 p.m.'), ('1:00 p.m.',
                                       '1:00 p.m.'), ('2:00 p.m.', '2:00 p.m.'),
        ('3:00 p.m.', '3:00 p.m.'), ('4:00 p.m.',
                                     '4:00 p.m.'), ('5:00 p.m.', '5:00 p.m.'),
        ('6:00 p.m.', '6:00 p.m.'), ('7:00 p.m.',
                                     '7:00 p.m.'), ('8:00 p.m.', '8:00 p.m.'),
    )
    order = models.ForeignKey(
        'orders.Order', on_delete=models.CASCADE, null=True
    )
    order_item = models.ForeignKey(
        'orders.OrderItem', on_delete=models.CASCADE, null=True
    )
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.CharField(max_length=10, choices=HOURS, blank=True)

    class Meta:
        ordering = ['date']
