# Generated by Django 4.0.6 on 2022-08-20 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_rename_user_buser'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BUser',
            new_name='User',
        ),
    ]
