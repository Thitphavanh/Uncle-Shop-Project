from django.urls import path, include
from .views import *

urlpatterns = [
    path("", home, name='home-page'),
    path('about/', about, name='about-page'),
    path('contact/', contact, name='contact-page'),
    path('addproduct/', add_product, name='add-product-page'),
    path('allproduct/', all_products, name='all-product-page'),
    path('register/', register, name='register-page'),
    path('addtocart/<int:pid>/', add_to_cart, name='add-to-cart-page'),
    path('mycart/', my_cart, name='my-cart-page'),
    path('mycartedit/', my_cart_edit, name='my-cart-edit-page'),
    path('checkout/', check_out, name='checkout-page'),
    path('orderproduct/', order_prodcut, name='order-product-page'),
    path('allorderproduct/', all_order_prodcut, name='all-order-product-page'),
    path('uploadslip/<str:orderid>/', upload_slip, name='upload-slip-page'),
    path('updatestatus/<str:orderid>/<str:status>/',
         update_paid, name='update-status-page'),
    path('updatetracking/<str:orderid>/',
         update_tracking, name='update-tracking-page'),
    path('myorder/<str:orderid>/', my_order, name='my-order-page'),
    path('category/<int:code>/', product_category,
         name='all-product-category-page'),
    path('graph/', pie_chart, name='graph-page'),
    path('productdetail/<int:productid>/',
         product_detail, name='product-detail-page'),
    path('editproduct/<int:productid>/', edit_product, name='edit-product-page'),
    path('api/allproductapi', all_product_api, name='all-product-api-page'),
    path('api/productapi/<int:pid>/',
         product_api, name='product-api-page'),
    path('api/getproductapi/<int:pid>/', get_product_api),
    path('api/postproductapi', post_product_api),
    path('api/updateproductapi/<int:pid>', update_product_api),
    path('api/deleteproductapi/<int:pid>', delete_product_api),
]

#       <!-- {% block content %} {% endblock content %} -->
