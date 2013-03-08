from django import template
from email.utils import parsedate_tz, mktime_tz
from datetime import datetime
from time import mktime

register = template.Library()

@register.filter
def strtotime(value):
    return datetime.fromtimestamp(mktime_tz(parsedate_tz(value)))