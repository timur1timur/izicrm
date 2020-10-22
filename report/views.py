from django.shortcuts import render
from orders.models import Order, Room, Customer, Contract, Payment
from common.utils import GetCusPay, GetStatOrderPeriod, GetStatOrderFinishPeriod
from django.db.models import Sum, Count
import datetime
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear
from itertools import chain
from operator import attrgetter



def ReportOrders(request):
    qs = Order.objects.all().order_by('-date_created')
    rooms = Room.objects.all()
    customer = Customer.objects.all()

    cus_pay_order = qs.filter(status__gte=5).order_by('-pk')
    cus_pay_dic = {}
    for q in cus_pay_order:
        q_m = {}
        number = q.number
        status = GetCusPay(q)[0]
        progress = GetCusPay(q)[1]

        q_m['status'] = status
        q_m['progress'] = progress
        q_m['ready'] = GetCusPay(q)[2]
        cus_pay_dic[number] = q_m

    order_cat_name = Order._meta.get_field('status').choices
    order_cat = qs.values('status').annotate(Count('status')).order_by('status')

    print(order_cat)
    print(order_cat_name)
    cus_label = []
    cus_data = []
    for c in order_cat:
        data = c['status__count']
        cus_data.append(data)
        label = c['status']
        for cat in order_cat_name:
            if label == cat[0]:
                cus_label.append(f"{cat[1]} - {data} шт.")

    cus_cat_name = Customer._meta.get_field('source_t').choices
    cus_cat = Customer.objects.all()
    cus_cat1 = cus_cat.values('source_t').annotate(Count('source_t')).order_by('source_t')

    cus_label2 = []
    cus_data2 = []
    for c in cus_cat1:
        data = c['source_t__count']
        cus_data2.append(data)
        label = c['source_t']
        for cat in cus_cat_name:
            if label == cat[0]:
                cus_label2.append(f"{cat[1]} - {data} шт.")

    print(cus_data2)
    print(cus_label2)


    end_n = datetime.datetime.now() + datetime.timedelta(days=1)
    end = end_n.strftime("%Y-%m-%d")
    end_s = end.split('-')
    start_n = end_n - datetime.timedelta(days=30)
    start = start_n.strftime("%Y-%m-%d")
    start_s = start.split('-')

    f = GetStatOrderPeriod(start, end)
    g = GetStatOrderFinishPeriod(start, end)

    period = str(start_n.strftime("%d.%m.%Y")) + ' - ' + str(end_n.strftime("%d.%m.%Y"))

    context = {
        'orders': qs,
        'room': rooms,
        'customer': customer,
        'order_test': cus_pay_dic,
        'cus_label': cus_label,
        'cus_data': cus_data,
        'cus_label2': cus_label2,
        'cus_data2': cus_data2,
        'data1': f[0],
        'qs_count1': f[1],
        'data2': g[0],
        'qs_count2': g[1],
        'period': period,
        'startDate': [int(start_s[0]),
                      int(start_s[1]) - 1,
                      int(start_s[2])],
        'endDate': [int(end_s[0]), int(end_s[1]) - 1,
                    int(end_s[2])],

    }
    return render(request, 'report/report_orders.html', context)


def ReportOrdersDate(request, start, end):
    start_s = start.split('-')
    start = datetime.date(int(start_s[0]), int(start_s[1]), int(start_s[2]))
    end_s = end.split('-')
    end = datetime.date(int(end_s[0]), int(end_s[1]), int(end_s[2])) + datetime.timedelta(days=1)
    qs = Order.objects.filter(date_created__gte=start, date_created__lte=end).order_by('-date_created')
    rooms = Room.objects.all()
    customer = Customer.objects.all()

    cus_pay_order = qs.filter(status__gte=5).order_by('-pk')
    cus_pay_dic = {}
    for q in cus_pay_order:
        q_m = {}
        number = q.number
        status = GetCusPay(q)[0]
        progress = GetCusPay(q)[1]

        q_m['status'] = status
        q_m['progress'] = progress
        q_m['ready'] = GetCusPay(q)[2]
        cus_pay_dic[number] = q_m

    order_cat_name = Order._meta.get_field('status').choices
    order_cat = qs.values('status').annotate(Count('status')).order_by('status')

    print(order_cat)
    print(order_cat_name)
    cus_label = []
    cus_data = []
    for c in order_cat:
        data = c['status__count']
        cus_data.append(data)
        label = c['status']
        for cat in order_cat_name:
            if label == cat[0]:
                cus_label.append(f"{cat[1]} - {data} шт.")

    cus_cat_name = Customer._meta.get_field('source_t').choices
    cus_cat = Customer.objects.filter(date_created__gte=start, date_created__lte=end)
    cus_cat1 = cus_cat.values('source_t').annotate(Count('source_t')).order_by('source_t')

    cus_label2 = []
    cus_data2 = []
    for c in cus_cat1:
        data = c['source_t__count']
        cus_data2.append(data)
        label = c['source_t']
        for cat in cus_cat_name:
            if label == cat[0]:
                cus_label2.append(f"{cat[1]} - {data} шт.")

    print(cus_data2)
    print(cus_label2)


    f = GetStatOrderPeriod(start, end)
    g = GetStatOrderFinishPeriod(start, end)

    period = str(start.strftime("%d.%m.%Y")) + ' - ' + str(end.strftime("%d.%m.%Y"))

    context = {
        'orders': qs,
        'room': rooms,
        'customer': customer,
        'order_test': cus_pay_dic,
        'cus_label': cus_label,
        'cus_data': cus_data,
        'cus_label2': cus_label2,
        'cus_data2': cus_data2,
        'data1': f[0],
        'qs_count1': f[1],
        'data2': g[0],
        'qs_count2': g[1],
        'period': period,
        'startDate': [int(start_s[0]),
                      int(start_s[1]) - 1,
                      int(start_s[2])],
        'endDate': [int(end_s[0]), int(end_s[1]) - 1,
                    int(end_s[2])],

    }
    return render(request, 'report/report_orders.html', context)


def ReportBudget(request):

    end_n = datetime.datetime.now() + datetime.timedelta(days=1)
    end_day = end_n.strftime("%d")
    start_n = end_n - datetime.timedelta(days=int(end_day)-1)
    end = end_n.strftime("%Y-%m-%d")
    start = start_n.strftime("%Y-%m-%d")
    orders = Order.objects.filter(date_created__gte=start, date_created__lte=end)

    date_list_start = []
    date_list_end = []
    date_normalize = []
    date_list = [end_n - datetime.timedelta(days=x) for x in range(1, int(end_day))]
    for d in date_list:
        date_list_start.append(d.strftime("%Y-%m-%d") + ' ' + '00:00')
        date_list_end.append(d.strftime("%Y-%m-%d") + ' ' + '23:59')
        date_normalize.append(d.strftime("%d.%m"))
    list_start = list(reversed(date_list_start))
    list_end = list(reversed(date_list_end))
    list_normalize = list(reversed(date_normalize))
    budget_mass = {}
    y = 0
    i = 0
    arrival_value1 = 0
    expense_value1 = 0
    profit_value1 = 0
    while i < len(list_start):
        contract = Contract.objects.filter(date_created__gte=list_start[y], date_created__lte=list_end[y]).aggregate(Sum('price'))
        payment = Payment.objects.filter(date_created__gte=list_start[y], date_created__lte=list_end[y], category__type_p=1).aggregate(Sum('price'))
        if contract['price__sum'] != None:
            if payment['price__sum'] != None:
                profit = contract['price__sum'] - payment['price__sum']
            else:
                profit = contract['price__sum']
                payment['price__sum'] = 0
        else:
            if payment['price__sum'] != None:
                profit = 0 - payment['price__sum']
                contract['price__sum'] = 0
            else:
                profit = 0
                payment['price__sum'] = 0
                contract['price__sum'] = 0

        arrival_value1 += contract['price__sum']
        expense_value1 += payment['price__sum']
        p = (arrival_value1 - expense_value1)
        if p != 0:
            profit_value1 = p
        else:
            profit_value1 = profit_value1

        budget_mass[list_normalize[y]] = {
                    'arrival': contract['price__sum'],
                    'expense': payment['price__sum'],
                    'profit': round(profit, 2),
                    'arrival_n': round(arrival_value1, 2),
                    'expense_n': round(expense_value1, 2),
                    'profit_n': round(profit_value1, 2)
                }
        y += 1
        i += 1
    print(budget_mass)

    date_m = []
    arrival_m = []
    expense_m = []
    arrival_value = 0
    expense_value = 0
    z = 0
    for q in budget_mass:
        if budget_mass[q]['arrival'] != None:
            arrival_value += budget_mass[q]['arrival']
        else:
            arrival_value += 0
        if budget_mass[q]['expense'] != None:
            expense_value += budget_mass[q]['expense']
        else:
            expense_value += 0

        arrival_m.append([z, round(budget_mass[q]['arrival'], 2)])
        expense_m.append([z, round(budget_mass[q]['expense'], 2)])
        date_m.append([z, q])
        z += 1

    max_mass = []
    for m in arrival_m:
        max_mass.append(m[1])
    period = str(start_n.strftime("%d.%m.%Y")) + ' - ' + str(end_n.strftime("%d.%m.%Y"))

    context = {
        'arrival_m': arrival_m,
        'expense_m': expense_m,
        'date_m': date_m,
        'max': max(max_mass) + 5000,
        'period': period,
        'budget_mass': budget_mass
    }

    return render(request, 'report/report_budget.html', context)


month_dict = {
    '1': 'Январь',
    '2': 'Февраль',
    '3': 'Март',
    '4': 'Апрель',
    '5': 'Май',
    '6': 'Июнь',
    '7': 'Июль',
    '8': 'Август',
    '9': 'Сентябрь',
    '10': 'Октябрь',
    '11': 'Ноябрь',
    '12': 'Декабрь',
}


def ReportBudgetMonth(request):

    end_n = datetime.datetime.now() + datetime.timedelta(days=1)
    end_month = end_n.strftime("%m")

    month_list = []
    i = 1
    while i <= int(end_month):
        month_list.append(i)
        i += 1
    print(month_list)
    budget_mass = {}
    y = 0
    while y < len(month_list):
        contract = Contract.objects.filter(date_created__month=month_list[y]).aggregate(Sum('price'))
        payment = Payment.objects.filter(date_created__month=month_list[y], category__type_p=1).aggregate(Sum('price'))

        if contract['price__sum'] != None:
            if payment['price__sum'] != None:
                profit = contract['price__sum'] - payment['price__sum']
            else:
                profit = contract['price__sum']
                payment['price__sum'] = 0
        else:
            if payment['price__sum'] != None:
                profit = 0 - payment['price__sum']
                contract['price__sum'] = 0
            else:
                profit = 0
                payment['price__sum'] = 0
                contract['price__sum'] = 0

        budget_mass[month_dict.get(str(month_list[y]))] = {
                    'arrival': contract['price__sum'],
                    'expense': payment['price__sum'],
                    'profit': round(profit, 2),
                }

        y += 1
    print(budget_mass)
    date_m = []
    arrival_m = []
    expense_m = []
    profit_m = []


    z = 0
    for q in budget_mass:

        arrival_m.append([z, round(budget_mass[q]['arrival'], 2)])
        expense_m.append([z, round(budget_mass[q]['expense'], 2)])
        profit_m.append([z, round(budget_mass[q]['profit'], 2)])
        date_m.append([z, month_list[z]])
        z += 1

    print(date_m)
    print(arrival_m)
    print(expense_m)
    print(profit_m)
    max_mass = []
    for m in arrival_m:
        max_mass.append(m[1])
    context = {
        'arrival_m': arrival_m,
        'expense_m': expense_m,
        'profit_m': profit_m,
        'date_m': date_m,
        'max': max(max_mass) + 50000,
        'budget_mass': budget_mass
    }

    return render(request, 'report/report_budget_month.html', context)

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()




def ReportUser(request):
    qs = User.objects.all()

    user_mass = {}

    for q in qs:
        orders = Order.objects.filter(user=q).all()
        orders_count = orders.count()
        contract_sum = 0
        if orders_count > 0:
            for ord in orders:
                if ord.status > 3:
                    contract = Contract.objects.get(order=ord)
                    print(contract)
                    contract_sum += contract.price

        user_mass[q.get_full_name()] = {
            'count': orders_count,
            'arrival': contract_sum,
        }
    print(user_mass)
    context = {
    }
    return render(request, 'report/report_orders.html', context)