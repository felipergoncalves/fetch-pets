from django import template
from django.utils.timesince import timesince as timesince_builtin
from django.utils.timezone import now

register = template.Library()

@register.filter
def timesince(value):
    return timesince_builtin(value, now())
