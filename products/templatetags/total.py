from django import template

register=template.Library()

@register.simple_tag(name='total')

def total(cart):
    total1=0
    for item in cart.added_items.all():
        total1+=item.quantity*item.product.price
    return total1