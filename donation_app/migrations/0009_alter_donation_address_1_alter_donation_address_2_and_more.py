# Generated by Django 4.0.4 on 2022-05-15 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donation_app', '0008_alter_donation_address_1_alter_donation_address_2_and_more'),
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
            model_name='donation',
            name='categories',
            field=models.ManyToManyField(to='donation_app.category'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='institution',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='donation_app.institution'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='donation',
            name='pick_up_comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
