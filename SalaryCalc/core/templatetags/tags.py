from django import template
from core.models import WorkCalendar

register = template.Library()


# ===== Filter =====
@register.filter
def keyvalue(dictionary, key):
    try:
        if dictionary[key] != None:
            return dictionary[key]
        return ''
    except Exception as e:
        return ''
# ===== END Filter =====
