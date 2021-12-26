# Generated by Django 3.2.9 on 2021-12-21 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20211222_0336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.CharField(choices=[('9', '9:00 a.m.'), ('10', '10:00 a.m.'), ('11', '11:00 a.m.'), ('12', '12:00 p.m.'), ('13', '1:00 p.m.'), ('14', '2:00 p.m.'), ('15', '3:00 p.m.'), ('16', '4:00 p.m.'), ('17', '5:00 p.m.'), ('18', '6:00 p.m.'), ('19', '7:00 p.m.'), ('20', '8:00 p.m.')], max_length=10, verbose_name='Delivery Time'),
        ),
    ]