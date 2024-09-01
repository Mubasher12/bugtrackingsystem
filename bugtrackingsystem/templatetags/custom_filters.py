from django import template

register = template.Library()

@register.filter
def dict_list(queryset, field_name):
    return [getattr(item, field_name) for item in queryset]

register = template.Library()

@register.filter
def add_class(value, class_name):
    return value.as_widget(attrs={'class': class_name})