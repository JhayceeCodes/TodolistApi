# Generated by Django 5.0 on 2024-01-09 02:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("todo", "0002_rename_complete_todo_completed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todo",
            name="completed",
            field=models.BooleanField(default=False),
        ),
    ]
