from django import template

register = template.Library()

@register.filter
def pipe_to_nl(value):
    return value.replace('|', "\n")
