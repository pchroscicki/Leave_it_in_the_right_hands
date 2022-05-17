# Generated by Django 4.0.4 on 2022-05-17 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation_app', '0012_donation_status_update_date_alter_donation_address_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='address_1',
            field=models.CharField(max_length=128, verbose_name=('address',)),
        ),
        migrations.AlterField(
            model_name='donation',
            name='address_2',
            field=models.CharField(blank=True, max_length=128, verbose_name=('address cd',)),
        ),
    ]
