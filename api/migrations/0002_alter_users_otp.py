# Generated by Django 4.2 on 2023-05-31 10:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="otp",
            field=models.IntegerField(),
        ),
    ]
