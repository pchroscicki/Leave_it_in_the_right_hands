from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField
from pkg_resources import _


class Category(models.Model):
    name = models.CharField(max_length=255)

class Institution(models.Model):
    #type to integer coding:
    FOUNDATION = 1
    NGO = 2
    LOCAL_CHARITY = 3

    TYPE_CHOICES = (
        (FOUNDATION, 'Foundation'),
        (NGO, 'Non-governmental organisation'),
        (LOCAL_CHARITY, 'Local charities and community groups'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    type = models.CharField(choices=TYPE_CHOICES, default=FOUNDATION, max_length=64)
    categories = models.ManyToManyField(Category)

class Donation(models.Model):
    quantity = models.SmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    address_1 = models.CharField(_("address"), max_length=128)
    address_2 = models.CharField(_("address cd"), max_length=128, blank=True)
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, default=None)
