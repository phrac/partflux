from django import template

register = template.Library()

@register.filter
def usernl2nl(value):
    return value.replace('\N', "\n")
