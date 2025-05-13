from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])

@register.filter
def until(value, end):
    """Возвращает range(value, end) для шаблонных циклов."""
    return range(value, end)
