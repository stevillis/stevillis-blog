# Generated by Django 5.2 on 2025-05-03 19:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="blog",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
