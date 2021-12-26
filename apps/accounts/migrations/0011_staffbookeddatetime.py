# Generated by Django 3.2.9 on 2021-12-23 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20211223_0542'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffBookedDateTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.CharField(blank=True, max_length=10)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.staff')),
            ],
        ),
    ]
