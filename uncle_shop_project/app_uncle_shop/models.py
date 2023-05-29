from email.policy import default
from django.db import models
from django.contrib.auth.models import User


class VerifyEmail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.user


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="photoprofile",
                              null=True, blank=True, default='default.png')
    usertype = models.CharField(max_length=100, default='member')
    cartquan = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name


class Category(models.Model):
    category_name = models.CharField(max_length=250, default='สินค้าทั่วไป')
    detail = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.category_name


class AllProduct(models.Model):
    category_name = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    detail = models.TextField(null=True, blank=True)
    imageurl = models.CharField(max_length=200, null=True, blank=True)
    instock = models.BooleanField(default=True)
    quantity = models.IntegerField(default=1)
    unit = models.CharField(max_length=200, default='-')
    images = models.ImageField(upload_to="products", null=True, blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    productid = models.CharField(max_length=100)
    productname = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    stamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    total = models.IntegerField()

    def __str__(self):
        return self.user


class OrderProduct(models.Model):
    orderid = models.CharField(max_length=100)
    productid = models.CharField(max_length=100)
    productname = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return self.orderid


class OrderPending(models.Model):
    orderid = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    address = models.TextField()
    shipping = models.CharField(max_length=100)
    payment = models.CharField(max_length=100)
    other = models.TextField(null=True, blank=True)
    stamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    paid = models.BooleanField(default=False)
    slip = models.ImageField(upload_to="slip", null=True, blank=True)
    slip_time = models.DateField(null=True, blank=True)
    bank_account = models.CharField(
        max_length=50,
        choices=[('KBank', 'KBank'), ('SCB', 'SCB'),
                 ('TTB', 'TTB'), ('KTB', 'KTB'),
                 ('BBL', 'BBL'), ('BAY', 'BAY'),
                 ('อื่นๆ', 'อื่นๆ'), ],
        default='KBank'
    )
    paymentid = models.CharField(max_length=100, null=True, blank=True)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.orderid
