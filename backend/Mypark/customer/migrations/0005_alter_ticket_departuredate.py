# Generated by Django 4.2.5 on 2023-09-16 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_ticket_fine_ticket_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='departureDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
