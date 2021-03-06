# Generated by Django 3.2.10 on 2022-03-06 21:32

from django.db import migrations

import celebrity.models


class Migration(migrations.Migration):

    dependencies = [
        ("celebrity", "0003_auto_20220306_2105"),
    ]

    operations = [
        migrations.AlterField(
            model_name="celebrity",
            name="phone_number",
            field=celebrity.models.PossiblePhoneNumberField(
                db_index=True, max_length=128, region=None, unique=True
            ),
        ),
    ]
