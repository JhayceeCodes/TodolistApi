# Generated by Django 5.0 on 2024-01-03 12:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("todo", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="todo",
            old_name="complete",
            new_name="completed",
        ),
    ]
