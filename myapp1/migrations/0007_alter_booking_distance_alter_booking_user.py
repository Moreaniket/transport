# Generated by Django 5.1.3 on 2025-01-07 05:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0006_alter_booking_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='distance',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='myapp1.customer'),
        ),
    ]
