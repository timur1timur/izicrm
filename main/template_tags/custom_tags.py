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

from materials.models import Cornice, CorniceAdditional, CorniceAdditionalOptions, Textile

@register.filter(name='get_additional')
def get_additional(cornice):
    cornice_g = Cornice.objects.get(pk=cornice)
    if CorniceAdditional.objects.filter(cornice=cornice_g):
        add_count = CorniceAdditional.objects.filter(cornice=cornice_g).count()
    else:
        add_count = 0
    return add_count


@register.filter(name='get_textile_count')
def get_textile_count(collection):
    textile_count = Textile.objects.filter(collection=collection).count()
    return textile_count

@register.filter(name='get_cornice_count')
def get_cornice_count(collection):
    cornice_count = Cornice.objects.filter(collection=collection).count()
    return cornice_count

@register.filter(name='get_additional_options_count')
def get_additional_options_count(additional):
    options_count = CorniceAdditionalOptions.objects.filter(additional=additional).count()
    return options_count

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

from markup.models import MarkupCurrency

@register.simple_tag()
def get_currency():
    usd = MarkupCurrency.objects.get(name='USD')
    eur = MarkupCurrency.objects.get(name='EUR')
    f = f'USD: {round(usd.value,2)} руб  EUR: {round(eur.value,2)} руб'
    return f




@register.filter(name='get_currency_price')
def get_currency_price(price, type):
    if type == 1:
        usd = MarkupCurrency.objects.get(name='USD')
        f_price = float(price) * float(usd.value)*1.03
    elif type == 2:
        eur = MarkupCurrency.objects.get(name='EUR')
        f_price = float(price) * float(eur.value) * 1.03

    return round(f_price, 2)


from orders.models import Room, Specification, OfferVersion, Offer, OrderItemWorkSewing, OrderItemWorkAssembly, \
    OrderItemWorkHanging, OrderItemWorkDelivery

@register.filter(name='get_f_order')
def get_f_order(id):
    order = Order.objects.get(pk=id)
    work = 0
    if order.status == 7:
        mass = []
        offers = Offer.objects.filter(order=order)
        for offer in offers:
            mass.append(offer.version.version)
        sewing = OrderItemWorkSewing.objects.filter(order=order, version=mass[0]).count()
        assembly = OrderItemWorkAssembly.objects.filter(order=order, version=mass[0]).count()
        hanging = OrderItemWorkHanging.objects.filter(order=order, version=mass[0]).count()
        delivery = OrderItemWorkDelivery.objects.filter(order=order, version=mass[0]).count()
        work += sewing+assembly+hanging+delivery
    return work

@register.simple_tag()
def get_finish_orders():
    result = Order.objects.filter(status=9).count()
    all_orders = Order.objects.filter(status=8)
    count_n = 0

    for ord in all_orders:
        work = 0
        mass = []
        offers = Offer.objects.filter(order=ord)
        for offer in offers:
            mass.append(offer.version.version)
        sewing = OrderItemWorkSewing.objects.filter(order=ord, version=mass[0]).count()
        assembly = OrderItemWorkAssembly.objects.filter(order=ord, version=mass[0]).count()
        hanging = OrderItemWorkHanging.objects.filter(order=ord, version=mass[0]).count()
        delivery = OrderItemWorkDelivery.objects.filter(order=ord, version=mass[0]).count()
        work += sewing + assembly + hanging + delivery
        if work == 0:
            count_n += 1
    return result+count_n