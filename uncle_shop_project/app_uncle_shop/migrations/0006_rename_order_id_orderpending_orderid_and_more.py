# Generated by Django 4.2.1 on 2023-05-15 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_uncle_shop", "0005_rename_product_id_cart_productid_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="orderpending", old_name="order_id", new_name="orderid",
        ),
        migrations.RenameField(
            model_name="orderproduct", old_name="order_id", new_name="orderid",
        ),
    ]
