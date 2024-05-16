from datetime import datetime, timedelta
from django import template

register = template.Library()
@register.filter(name='add_duration')
def add_duration(value, arg):
    """Adds duration based on the jenis_paket."""
    try:
        base_datetime = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        if arg == "1 bulan":
            return (base_datetime + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
        elif arg == "3 bulan":
            return (base_datetime + timedelta(days=90)).strftime("%Y-%m-%d %H:%M:%S")
        elif arg == "6 bulan":
            return (base_datetime + timedelta(days=180)).strftime("%Y-%m-%d %H:%M:%S")
        elif arg == "1 tahun":
            return (base_datetime + timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return value 