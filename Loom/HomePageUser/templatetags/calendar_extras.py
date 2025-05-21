from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])

@register.filter
def until(value, end):
    """Возвращает range(value, end) для шаблонных циклов."""
    return range(value, end)

@register.filter
def category_to_color_class(category):
    mapping = {
        'Работа/Учёба': 'blue-task',
        'Бытовые дела': 'purple-task',
        'Время, проведённое с семьёй': 'green-task',
        'Время, проведённое с друзьями': 'orange-task',
        'Личные дела': 'red-task',
        'Праздники': 'yellow-task',
        'Тег: Важно': 'priority-high',
        'Тег: Обычное': 'priority-normal',
        'Тег: Низкий приоритет': 'priority-low',
        'Синий': 'blue-task',
        'Фиолетовый': 'purple-task',
        'Зелёный': 'green-task',
        'Оранжевый': 'orange-task',
        'Красный': 'red-task',
        'Жёлтый': 'yellow-task',
    }
    return mapping.get(category, 'blue-task')
