# Generated by Django 4.2.1 on 2023-05-15 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_uncle_shop", "0003_orderproduct_orderpending_cart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderpending",
            name="bank_account",
            field=models.CharField(
                choices=[
                    ("KBank", "KBank"),
                    ("SCB", "SCB"),
                    ("TTB", "TTB"),
                    ("KTB", "KTB"),
                    ("BBL", "BBL"),
                    ("BAY", "BAY"),
                    ("อื่นๆ", "อื่นๆ"),
                ],
                default="KBank",
                max_length=50,
            ),
        ),
    ]