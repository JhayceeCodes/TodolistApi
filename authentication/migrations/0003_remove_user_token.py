# Generated by Django 5.0 on 2023-12-28 19:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0002_user_token"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="token",
        ),
    ]
