# Generated by Django 4.1.10 on 2025-02-28 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0018_booking_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('number', models.IntegerField()),
                ('servicetype', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=1000)),
            ],
        ),
    ]
