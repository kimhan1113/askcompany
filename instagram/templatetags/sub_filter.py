from datetime import datetime, timedelta

from django import template
from django.utils import timezone
from datetime import datetime, timedelta,date


from django.utils.timesince import timesince

from instagram.models import Post

register = template.Library()

@register.filter
def get_type(value):
    return type(value)

@register.filter()
def addDays(days):
   newDate = date.today() + timedelta(days=days)
   return newDate


@register.filter
def days_until(date):
    delta = datetime.date(date) - datetime.now().date()
    return delta.days

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter()
def to_int(value):
    return int(value)