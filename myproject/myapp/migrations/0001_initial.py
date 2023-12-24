# Generated by Django 5.0 on 2023-12-24 18:21

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("price", models.IntegerField(default=0)),
                ("currency", models.CharField(default="RUB", max_length=10)),
                ("archived", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("discount", models.CharField(max_length=3)),
                ("tax", models.CharField(max_length=3)),
                ("items", models.ManyToManyField(to="myapp.item")),
            ],
        ),
    ]
