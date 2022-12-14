# Generated by Django 4.0.6 on 2022-08-24 05:19

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0019_rename_stripe_charge_id_payment_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 24, 5, 19, 46, 300600, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
