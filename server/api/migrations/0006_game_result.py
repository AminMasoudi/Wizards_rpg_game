# Generated by Django 4.2.1 on 2023-07-07 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_player_last_action"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="result",
            field=models.JSONField(null=True),
        ),
    ]