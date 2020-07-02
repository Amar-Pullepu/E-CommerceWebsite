from django import template
from home.models import Order
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.filter(name='col')
def col(value, arg):
    return list(value.__dict__.values())[-2+int(arg)]

@register.filter(name='inside')
def inside(value, arg):
    return value in arg.keys()

@register.filter(name='get')
def value(value, arg):
    return value[arg]

@register.filter(name='cart_count')
def cart_item_count(user):
    if user.is_authenticated:
        try:
            order = Order.objects.get(user=user, ordered=False)
            return order.items.count()
        except ObjectDoesNotExist:
            return 0
    return None