# Generated by Django 4.0.4 on 2022-05-28 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation_app', '0013_alter_donation_address_1_alter_donation_address_2'),
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