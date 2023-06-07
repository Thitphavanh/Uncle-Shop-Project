from rest_framework import serializers
from .models import *


class AllProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = AllProduct
        fields = ("id", "category_name", "name", "price", "detail", "quantity")
