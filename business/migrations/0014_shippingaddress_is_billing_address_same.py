# Generated by Django 4.0.6 on 2022-08-23 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0013_billingaddress_shippingaddress_checkout'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='is_billing_address_same',
            field=models.BooleanField(default=False),
        ),
    ]
