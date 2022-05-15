from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField
from pkg_resources import _


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        """String for representing Category objects in Admin site."""
        return self.name

class Institution(models.Model):
    TYPE_CHOICES = (
        ('FOUNDATION', 'Foundation'),
        ('NON-GOVERNMENTAL ORGANISATION', 'Non-governmental organisation'),
        ('LOCAL CHARITY', 'Local charities and community groups'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    type = models.CharField(choices=TYPE_CHOICES, default='FOUNDATION', max_length=64)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        """String for representing Institution objects in Admin site."""
        return self.name

class Donation(models.Model):
    quantity = models.SmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(null=False, blank=False)
    address_1 = models.CharField(_("address"), max_length=128)
    address_2 = models.CharField(_("address cd"), max_length=128, blank=True)
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, default=None)
