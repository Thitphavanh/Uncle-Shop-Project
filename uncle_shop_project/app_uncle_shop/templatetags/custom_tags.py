from django import template
from ..models import *


register = template.Library()


@register.simple_tag
def hello_tag():
    return "<-----Hello tag----->"


@register.simple_tag
def show_all_product():
    count = AllProduct.objects.count()
    return count


@register.inclusion_tag("app_uncle_shop/all-category.html")
def all_category():
    category = Category.objects.all()
    return {"categories": category}
