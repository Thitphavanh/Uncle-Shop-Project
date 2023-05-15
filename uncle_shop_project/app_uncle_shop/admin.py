from django.contrib import admin
from .models import *


admin.site.site_header = "Uncle Shop Official Website"
admin.site.index_title = "Main Admin"


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'photo', 'cartquan']
    list_editable = ['photo', 'cartquan']


admin.site.register(Profile, ProfileAdmin)


class AllProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'instock']
    list_editable = ['price', 'instock']


admin.site.register(AllProduct, AllProductAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'price', 'quantity']
    list_editable = ['price', 'quantity']


admin.site.register(Cart, CartAdmin)


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'quantity']
    list_editable = ['price', 'quantity']


admin.site.register(OrderProduct, OrderProductAdmin)


class OrderPendingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'tel', 'payment']
    list_editable = ['name', 'tel']


admin.site.register(OrderPending, OrderPendingAdmin)
