from django import template

from app.models import *

register=template.Library()

@register.simple_tag
def catrgories_tag():
    return Category.objects.all()
