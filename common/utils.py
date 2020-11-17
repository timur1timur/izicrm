from orders.models import Order, Payment, Offer, OrderItemTextile1, OrderItemCornice, OrderItemWorkSewing, \
    OrderItemWorkAssembly, OrderItemWorkHanging, OrderItemWorkDelivery, Contract

def Get_Budget(id):
    qs = Order.objects.get(pk=id)
    payments_arrival = Payment.objects.filter(order=qs, type_p=0)
    payments_expense = Payment.objects.filter(order=qs, type_p=1)
    offer = Offer.objects.get(order=qs)
    offer_version = offer.version.get_version_display()
    textile = OrderItemTextile1.objects.filter(order=qs, version=offer_version)
    cornice = OrderItemCornice.objects.filter(order=qs, version=offer_version)
    sewing = OrderItemWorkSewing.objects.filter(order=qs, version=offer_version)
    assembly = OrderItemWorkAssembly.objects.filter(order=qs, version=offer_version)
    hanging = OrderItemWorkHanging.objects.filter(order=qs, version=offer_version)
    delivery = OrderItemWorkDelivery.objects.filter(order=qs, version=offer_version)

    textile_arrival = 0
    textile_expense = 0
    for t in textile:
        textile_arrival += t.total_price()
        textile_expense += t.item.price_opt * t.quantity

    cornice_arrival = 0
    cornice_expense = 0
    for t in cornice:
        cornice_arrival += t.total_price()
        cornice_expense += t.item.price_opt * t.quantity

    sewing_arrival = 0
    sewing_expense = 0
    for t in sewing:
        sewing_arrival += t.total_price()
        sewing_expense += t.item.price * t.quantity

    assembly_arrival = 0
    assembly_expense = 0
    for t in assembly:
        assembly_arrival += t.total_price()
        assembly_expense += t.item.price * t.quantity

    hanging_arrival = 0
    hanging_expense = 0
    for t in hanging:
        hanging_arrival += t.total_price()
        hanging_expense += t.item.price * t.quantity

    delivery_arrival = 0
    delivery_expense = 0
    for t in delivery:
        delivery_arrival += t.total_price()
        delivery_expense += t.item.price * t.quantity

    total_arrival = textile_arrival + cornice_arrival + sewing_arrival + assembly_arrival + hanging_arrival + delivery_arrival
    total_expense = textile_expense + cornice_expense + sewing_expense + assembly_expense + hanging_expense + delivery_expense


    budget_plane = {
        'textile': {
            'arrival': textile_arrival,
            'expense': textile_expense
        },
        'cornice': {
            'arrival': cornice_arrival,
            'expense': cornice_expense
        },
        'sewing': {
            'arrival': sewing_arrival,
            'expense': sewing_expense
        },
        'assembly': {
            'arrival': assembly_arrival,
            'expense': assembly_expense
        },
        'hanging': {
            'arrival': hanging_arrival,
            'expense': hanging_expense
        },
        'delivery': {
            'arrival': delivery_arrival,
            'expense': delivery_expense
        },
        'total': {
            'arrival': round(total_arrival, 2),
            'expense': round(total_expense, 2),
            'profit': round((total_arrival - total_expense), 2),
            'change': round((total_arrival*100/total_expense), 2)
        }
    }

    pay_arrival = 0
    for t in payments_arrival:
        pay_arrival += float(t.price)
    pay_expense = 0
    for t in payments_expense:
        pay_expense += float(t.price)

    if pay_expense == 0:
        pay_change = 0
    else:
        pay_change = round((pay_arrival*100/pay_expense), 2)


    budget_fact = {
        'total': {
            'arrival': round(pay_arrival, 2),
            'expense': round(pay_expense, 2),
            'profit': round((pay_arrival - pay_expense), 2),
            'change': pay_change
        }
    }

    context = {
        'budget_plane': budget_plane,
        'budget_fact': budget_fact
    }
    return context

def GetStatusOrder(orders, id):
    return orders.filter(status=id)


import datetime
from django.db.models import Count
from django.db.models.functions import ExtractDay, ExtractMonth
from django.utils import timezone


def GetStatOrderPeriod(start, end):
    qs_count = Order.objects.filter(date_created__gte=start, date_created__lte=end).count()
    qs = Order.objects.filter(
        date_created__gte=start,
        date_created__lte=end
    ).annotate(
        day=ExtractDay('date_created'),
    ).values(
        'day'
    ).annotate(
        n=Count('pk')
    ).order_by('day')

    q_mass = {}
    for q in qs:
        q_mass[q['day']] = q['n']

    date_list_finish = []
    date_list_full = []
    base = datetime.datetime.now()
    date_list = [base - datetime.timedelta(days=x) for x in range(0, 30)]
    for d in date_list:
        date_list_finish.append(int(d.strftime("%d")))
        date_list_full.append(d.strftime("%d-%m-%Y"))
    list_date = list(reversed(date_list_finish))
    l = list(reversed(date_list_full))
    q_date = []
    q_finish = []
    d = list_date
    i = 30
    y = 0
    while y < i:
        try:
            if d[y] in q_mass:
                q_finish.append([y, q_mass.get(d[y])])
                q_date.append([y, d[y]])
                y += 1
            else:
                q_finish.append([y, 0.1])
                q_date.append([y, d[y]])
                y += 1

        except:
            q_finish.append([y, 0.1])
            y += 1
    print(q_finish)
    print(q_date)
    print(qs_count)
    return q_finish, qs_count

def GetStatOrderFinishPeriod(start, end):
    qs_count = Order.objects.filter(date_finished__gte=start, date_finished__lte=end).count()
    qs = Order.objects.filter(
        date_finished__gte=start,
        date_finished__lte=end
    ).annotate(
        day=ExtractDay('date_created'),
    ).values(
        'day'
    ).annotate(
        n=Count('pk')
    ).order_by('day')

    q_mass = {}
    for q in qs:
        q_mass[q['day']] = q['n']

    date_list_finish = []
    base = datetime.datetime.now()
    date_list = [base - datetime.timedelta(days=x) for x in range(0, 30)]
    for d in date_list:
        date_list_finish.append(int(d.strftime("%d")))
    list_date = list(reversed(date_list_finish))
    q_finish = []
    q_date = []
    d = list_date
    i = 30
    y = 0
    while y < i:
        try:
            if d[y] in q_mass:
                q_finish.append([y, q_mass.get(d[y])])
                q_date.append([y, d[y]])
                y += 1
            else:
                q_finish.append([y, 0.1])
                q_date.append([y, d[y]])
                y += 1

        except:
            q_finish.append([y, 0.1])
            y += 1

    return q_finish, qs_count

from django.db.models import Sum, Count


def GetCusPay(order):
    contract = Contract.objects.get(order=order)
    payments = Payment.objects.filter(order=order, category__type_p=0).aggregate(Sum('price'))
    val1 = f'{payments["price__sum"]} / {contract.price}'
    val2 = round(float(payments["price__sum"])*100/float(contract.price), 2)
    if round(float(contract.price), 2) == round(float(payments["price__sum"]), 2):
        val3 = 1
    else:
        val3 = 0
    return val1, val2, val3

import requests

def get_currency_now():
    res = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    usd = res.json()['Valute']['USD']['Value']
    eur = res.json()['Valute']['EUR']['Value']
    mass = {
        'usd': round(usd, 2),
        'eur': round(eur, 2)
    }
    return mass