# Generated by Django 4.2.1 on 2023-06-01 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_uncle_shop", "0010_alter_category_category_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderpending",
            name="confirmed",
            field=models.BooleanField(default=False),
        ),
    ]
