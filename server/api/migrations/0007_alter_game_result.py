# Generated by Django 4.2.1 on 2023-07-07 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_game_result"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="result",
            field=models.JSONField(default={}),
        ),
    ]