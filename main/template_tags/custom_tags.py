from django.template.defaulttags import register
from orders.models import Order

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_key(dictionary, key):
    return dictionary.keys(key)

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.simple_tag()
def get_new_orders():
    result = Order.objects.filter(status__gte=5, user_view=0).count()
    return result

@register.simple_tag()
def get_discount():
    result = Order.objects.filter(status__lte=3, discount_status=1, discount_view=0).count()
    return result

@register.simple_tag()
def get_finish_orders():
    result = Order.objects.filter(status=9).count()
    return result

@register.simple_tag()
def get_status_order():
    result = Order.objects.filter(status=9).count()
    return result

@register.filter
def get_short_name(name):
    new_n = name.split(' ')
    if len(new_n) > 2:
        short = new_n[0] + ' ' + new_n[1]
        return short
    else:
        return name

@register.filter(name='get_markup')
def get_markup(markup):
    markup_p = markup*100 - 100
    return f'{round(markup_p,2)} %'



@register.simple_tag()
def get_profit_position(total, price, quantity):
    result = float(total) - (float(price)*int(quantity))
    return round(result, 2)

from storage.models import StorageItemTextile, StorageItemTextileReserve
from django.db.models import Sum

@register.simple_tag()
def get_storage_item(id):
    storage_item = StorageItemTextile.objects.get(pk=id)
    reserve = StorageItemTextileReserve.objects.filter(item=storage_item).aggregate(Sum('quantity'))['quantity__sum']
    if reserve != None:
        result = storage_item.quantity - reserve
    else:
        result = storage_item.quantity
    return result