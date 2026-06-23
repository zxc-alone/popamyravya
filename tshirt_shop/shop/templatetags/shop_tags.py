from django import template
from shop.models import Category

register = template.Library()

@register.simple_tag
def get_categories():
    """Получение всех категорий"""
    return Category.objects.all()