
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('app_uncle_shop.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='app_uncle_shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='app_uncle_shop/logout.html'), name='logout'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
