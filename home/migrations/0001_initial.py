# Generated by Django 5.2 on 2025-04-28 12:53

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                ("blog_id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=200)),
                ("meta", models.CharField(max_length=300)),
                ("content", models.TextField()),
                (
                    "thumbnail_img",
                    models.ImageField(blank=True, null=True, upload_to="images/"),
                ),
                ("thumbnail_path", models.URLField(blank=True, null=True)),
                ("category", models.CharField(max_length=100)),
                ("slug", models.CharField(max_length=100)),
                ("created_at", models.DateField(auto_now_add=True)),
            ],
        ),
    ]
