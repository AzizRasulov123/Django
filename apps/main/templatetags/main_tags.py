from apps.main.models import Category, FAQ

from django.template import Library

register = Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.simple_tag()
def get_faqs():
    return FAQ.objects.all()