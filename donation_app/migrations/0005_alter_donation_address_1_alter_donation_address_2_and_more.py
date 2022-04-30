# Generated by Django 4.0.4 on 2022-04-29 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation_app', '0004_alter_donation_address_1_alter_donation_address_2_and_more'),
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
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.IntegerField(choices=[(1, 'Foundation'), (2, 'Non-governmental organisation'), (3, 'Local charities and community groups')], default=1),
        ),
    ]