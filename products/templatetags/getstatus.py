from django import template

register = template.Library()

@register.simple_tag(name='getstatus')
def getstatus(status):
    status_array = ['confirmed', 'processed', 'delivered', 'rejected']
    status = status - 1  # Adjust status to zero-based index
    return status_array[status] if 0 <= status < len(status_array) else 'Unknown'
