# Generated by Django 5.1.3 on 2025-01-06 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='confpassword',
        ),
    ]
