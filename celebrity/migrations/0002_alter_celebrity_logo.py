# Generated by Django 3.2.10 on 2022-03-03 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("celebrity", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="celebrity",
            name="logo",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]