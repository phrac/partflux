from django import template

register = template.Library()

@register.filter
def strip_dashes(value):
    return value.replace('-', '')
