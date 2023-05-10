from django.shortcuts import render
from .models import *


def home(request):
    product = AllProduct.objects.all().order_by('id').reverse()[:3]
    preorder = AllProduct.objects.filter(quantity__lte=0)
    context = {'product': product, 'preorder': preorder}
    return render(request, 'app_uncle_shop/home.html', context)
