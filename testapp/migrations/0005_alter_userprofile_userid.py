# Generated by Django 4.0.6 on 2022-08-25 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0004_userprofile_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='userid',
            field=models.CharField(max_length=10),
        ),
    ]
