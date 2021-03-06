# Generated by Django 3.2.10 on 2022-03-06 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("celebrity", "0002_alter_celebrity_logo"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="celebrity",
            name="instagram_link",
        ),
        migrations.RemoveField(
            model_name="celebrity",
            name="twitter_link",
        ),
        migrations.RemoveField(
            model_name="celebrity",
            name="website",
        ),
        migrations.AddField(
            model_name="celebrity",
            name="instagram_url",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="celebrity",
            name="twitter_url",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="celebrity",
            name="website_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
