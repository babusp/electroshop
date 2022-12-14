# Generated by Django 4.0.6 on 2022-08-18 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=100)),
                ('phone_no', models.CharField(blank=True, max_length=17, null=True, unique=True)),
                ('business_name', models.CharField(max_length=100)),
                ('business_type', models.CharField(max_length=100)),
                ('business_id', models.CharField(max_length=100, unique=True)),
                ('location', models.CharField(max_length=200)),
                ('is_verified', models.BooleanField(default=False)),
            ],
        ),
    ]
