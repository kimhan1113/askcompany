from django import template

register = template.Library()

@register.filter()
def get_field_name(object, field):
    verbose_name = object.get_field(field).verbose_name
    return verbose_name