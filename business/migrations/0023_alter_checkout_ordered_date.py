# Generated by Django 4.0.6 on 2022-08-25 03:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0022_alter_checkout_ordered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='ordered_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 25, 3, 58, 40, 213791, tzinfo=utc)),
        ),
    ]
