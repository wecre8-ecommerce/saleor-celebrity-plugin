# Generated by Django 3.2.10 on 2022-03-02 07:23

import django_countries.fields
from django.db import migrations, models

import celebrity.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Celebrity",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(db_index=True, max_length=256)),
                ("last_name", models.CharField(db_index=True, max_length=256)),
                (
                    "phone_number",
                    celebrity.models.PossiblePhoneNumberField(
                        db_index=True, max_length=128, region=None
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("country", django_countries.fields.CountryField(max_length=2)),
                ("city", models.CharField(blank=True, max_length=256, null=True)),
                ("website", models.TextField(blank=True, null=True)),
                ("instagram_link", models.TextField(blank=True, null=True)),
                ("twitter_link", models.TextField(blank=True, null=True)),
                ("bio", models.TextField(blank=True, null=True)),
                ("about", models.TextField(blank=True, null=True)),
                ("is_active", models.BooleanField()),
                ("logo", models.ImageField(upload_to="")),
                (
                    "header_image",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
