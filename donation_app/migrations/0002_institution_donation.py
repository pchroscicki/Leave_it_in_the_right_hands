# Generated by Django 4.0.4 on 2022-04-27 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('donation_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('type', models.CharField(choices=[(1, 'Foundation'), (2, 'Non-governmental organisation'), (3, 'Local charities and community groups')], default=1, max_length=64)),
                ('categories', models.ManyToManyField(to='donation_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField()),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('address_1', models.CharField(max_length=128, verbose_name=('address',))),
                ('address_2', models.CharField(blank=True, max_length=128, verbose_name=('address cd',))),
                ('city', models.CharField(max_length=128)),
                ('zip_code', models.CharField(max_length=6)),
                ('pick_up_date', models.DateField()),
                ('pick_up_time', models.TimeField()),
                ('pick_up_comment', models.TextField()),
                ('categories', models.ManyToManyField(to='donation_app.category')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donation_app.institution')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]