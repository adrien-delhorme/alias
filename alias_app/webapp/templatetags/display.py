from django import template

register = template.Library()


@register.filter(name='display')
def display_value(field):
    """Returns the display value of a BoundField"""
    return dict(field.field.choices).get(int(field.value()), '')
