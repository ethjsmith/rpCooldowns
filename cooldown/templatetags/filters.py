from django import template
register = template.Library()

@register.filter(name="times")
def times(number):
    if number == None:
        return [0]
    return range(number)

@register.filter(name="iter")
def iter(obj):
    if hasattr(obj,'__iter__'):
        return True
    return False
