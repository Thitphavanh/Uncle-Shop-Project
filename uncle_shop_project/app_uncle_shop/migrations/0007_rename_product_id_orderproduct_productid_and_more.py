# Generated by Django 4.2.1 on 2023-05-23 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_uncle_shop", "0006_rename_order_id_orderpending_orderid_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="orderproduct", old_name="product_id", new_name="productid",
        ),
        migrations.RenameField(
            model_name="orderproduct", old_name="product_name", new_name="productname",
        ),
    ]