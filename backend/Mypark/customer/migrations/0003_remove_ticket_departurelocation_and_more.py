# Generated by Django 4.2.5 on 2023-09-16 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_remove_ticket_parking_ticket_parking_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='departureLocation',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='destinationLocation',
        ),
    ]