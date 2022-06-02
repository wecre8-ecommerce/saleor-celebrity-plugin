from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from saleor.account.validators import validate_possible_number
from saleor.product.models import Product


class PossiblePhoneNumberField(PhoneNumberField):
    default_validators = [validate_possible_number]


class Celebrity(models.Model):

    first_name = models.CharField(max_length=256, db_index=True, null=True, blank=True)
    last_name = models.CharField(max_length=256, db_index=True, null=True, blank=True)
    phone_number = PossiblePhoneNumberField(db_index=True, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    country = CountryField(default="SA")
    city = models.CharField(max_length=256, blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    is_active = models.BooleanField()
    logo = models.ImageField(blank=True, null=True)
    header_image = models.ImageField(blank=True, null=True)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
