# Generated by Django 5.0.7 on 2025-02-28 11:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0002_text_post"),
    ]

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=100)),
                ("content", models.CharField(max_length=500)),
            ],
        ),
    ]
