from django import template

register = template.Library()

@register.filter # register the template filter with django
def str_to_arr(value): # Only one argument.
    return value.split(',')