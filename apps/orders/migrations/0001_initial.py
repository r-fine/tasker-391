# Generated by Django 3.2.9 on 2021-12-13 01:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=11, verbose_name='Phone Number')),
                ('email', models.EmailField(
                    max_length=100, verbose_name='Email Address')),
                ('address_line_1', models.CharField(max_length=255)),
                ('address_line_2', models.CharField(blank=True, max_length=255)),
                ('area', models.CharField(choices=[('Abdullahpur', 'Abdullahpur'), ('Agargaon', 'Agargaon'), ('Badda', 'Badda'), ('Banani', 'Banani'), ('Banasree', 'Banasree'), ('Baridhara', 'Baridhara'), ('Bashundhara', 'Bashundhara'), ('Bawnia', 'Bawnia'), ('Beraid', 'Beraid'), ('Cantonment area', 'Cantonment area'), ('Dakshinkhan', 'Dakshinkhan'), ('Dania', 'Dania'), ('Demra', 'Demra'), ('Dhanmondi', 'Dhanmondi'), ('Farmgate', 'Farmgate'), ('Gabtali', 'Gabtali'), ('Gulshan', 'Gulshan'), ('Hazaribagh', 'Hazaribagh'), ('Islampur', 'Islampur'), ('Jurain', 'Jurain'), ('Kafrul', 'Kafrul'), ('Kamalapur', 'Kamalapur'), ('Kamrangirchar', 'Kamrangirchar'), ('Kazipara', 'Kazipara'), (
                    'Khilgaon', 'Khilgaon'), ('Khilkhet', 'Khilkhet'), ('Kotwali', 'Kotwali'), ('Lalbagh', 'Lalbagh'), ('Matuail', 'Matuail'), ('Mirpur', 'Mirpur'), ('Mohakhali', 'Mohakhali'), ('Mohammadpur', 'Mohammadpur'), ('Motijheel', 'Motijheel'), ('Nimtoli', 'Nimtoli'), ('Pallabi', 'Pallabi'), ('Paltan', 'Paltan'), ('Ramna', 'Ramna'), ('Rampura', 'Rampura'), ('Sabujbagh', 'Sabujbagh'), ('Sadarghat', 'Sadarghat'), ('Satarkul', 'Satarkul'), ('Shahbagh', 'Shahbagh'), ('Sher-e-Bangla Nagar', 'Sher-e-Bangla Nagar'), ('Shyampur', 'Shyampur'), ('Sutrapur', 'Sutrapur'), ('Tejgaon', 'Tejgaon'), ('Uttara', 'Uttara'), ('Uttarkhan', 'Uttarkhan'), ('Vatara', 'Vatara'), ('Wari', 'Wari')], max_length=50)),
                ('order_note', models.CharField(blank=True, max_length=100)),
                ('date', models.DateField(verbose_name='Delivery Date')),
                ('time', models.TimeField(verbose_name='Delivery Time')),
                ('is_ordered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True,
                 on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ordered', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), (
                    'Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('assigned_staff', models.ForeignKey(blank=True, null=True,
                 on_delete=django.db.models.deletion.SET_NULL, to='accounts.staff')),
                ('order', models.ForeignKey(blank=True, null=True,
                 on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('service_option', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='services.serviceoption')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-order'],
            },
        ),
    ]
