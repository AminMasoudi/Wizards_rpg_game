# Generated by Django 4.2.1 on 2023-07-05 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Roles",
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
                ("name", models.CharField(max_length=15)),
                ("power", models.PositiveIntegerField(default=5)),
                ("magic", models.PositiveIntegerField(default=5)),
                ("mrr", models.PositiveIntegerField(default=10)),
                ("ef_defend", models.PositiveIntegerField(default=50)),
                ("ef_hit", models.PositiveIntegerField(default=50)),
                ("ef_magic", models.PositiveIntegerField(default=50)),
            ],
        ),
    ]