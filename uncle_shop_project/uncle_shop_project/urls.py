
from django.contrib import admin
from django.urls import path, include
from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('app_uncle_shop.urls')),
]
