from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    if hasattr(value, 'as_widget'):  # Check if value has the as_widget method
        return value.as_widget(attrs={'class': arg})
    else:
        return value  # Return the value unchanged if it doesn't have as_widget
