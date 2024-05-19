from django import template

register = template.Library()

@register.filter
def format_duration(duration):
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    
    formatted_duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    return formatted_duration