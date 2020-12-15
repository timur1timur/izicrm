from django.shortcuts import render, redirect, HttpResponse
from orders.models import Payment, PaymentCategory, Order
from orders.forms import PaymentFormDirector
import datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def ControlPayments(request):
    end_n = datetime.datetime.now() + datetime.timedelta(days=1)
    end = end_n.strftime("%Y-%m-%d")
    end_s = end.split('-')
    start_n = end_n - datetime.timedelta(days=30)
    start = start_n.strftime("%Y-%m-%d")
    start_s = start.split('-')

    qs = Payment.objects.filter(category__type_p=1,
                                date_created__gte=start,
                                date_created__lte=end).order_by('-date_created')

    qc = PaymentCategory.objects.all()


    cat_label = []
    cat_price = []
    for q in qc:

        qs_cat = qs.filter(category=q).aggregate(Sum('price'))
        if qs_cat['price__sum'] != None:
            cat_price.append(qs_cat['price__sum'])
            cat_label.append(f"{q.name} - {qs_cat['price__sum']} руб")

    period = str(start_n.strftime("%d.%m.%Y")) + ' - ' + str(end_n.strftime("%d.%m.%Y"))

    return render(request, 'director/payments.html',
                  context={'orders': qs,
                           'period': period,
                           'startDate': [int(start_s[0]),int(start_s[1])-1,int(start_s[2])],
                           'endDate': [int(end_s[0]),int(end_s[1])-1,int(end_s[2])],
                           'cat_label': cat_label,
                           'cat_price': cat_price,
                           'category': qc})

@login_required(login_url='login')
def ControlPaymentsDate(request, start, end):
    start_s = start.split('-')
    start = datetime.date(int(start_s[0]), int(start_s[1]), int(start_s[2]))
    end_s = end.split('-')
    end = datetime.date(int(end_s[0]), int(end_s[1]), int(end_s[2])) + datetime.timedelta(days=1)

    qs = Payment.objects.filter(category__type_p=1,
                                date_created__gte=start,
                                date_created__lte=end).order_by('-date_created')

    qc = PaymentCategory.objects.all()

    cat_label = []
    cat_price = []
    for q in qc:
        qs_cat = qs.filter(category=q).aggregate(Sum('price'))
        if qs_cat['price__sum'] != None:
            cat_price.append(qs_cat['price__sum'])
            cat_label.append(f"{q.name} - {qs_cat['price__sum']} руб")
    period = str(start.strftime("%d.%m.%Y")) + ' - ' + str((end - datetime.timedelta(days=1)).strftime("%d.%m.%Y"))
    return render(request, 'director/payments.html',
                  context={'orders': qs,
                           'period': period,
                           'startDate': [int(start_s[0]), int(start_s[1])-1, int(start_s[2])],
                           'endDate':   [int(end_s[0]), int(end_s[1])-1, int(end_s[2])],
                           'cat_label': cat_label,
                           'cat_price': cat_price
                           })

@login_required(login_url='login')
def PaymentCreate(request):

    if request.method == 'GET':
        form = PaymentFormDirector()
        return render(request, 'director/payment_create.html', context={'form': form})

    if request.method == 'POST':
        form = PaymentFormDirector(request.POST)
        category = request.POST.get("category", None)
        type_money = request.POST.get("type_money", None)
        price = request.POST.get("price", None)
        receipt = request.POST.get("receipt", None)
        order = request.POST.get("order", None)

        if category != None and type_money != None and price != None and receipt != None:
            cat = PaymentCategory.objects.get(pk=category)
            if cat.pk == 9:
                order_g = Order.objects.get(pk=order)
                instance = Payment.objects.create(
                    category=cat,
                    type_money=type_money,
                    price=price,
                    receipt=receipt,
                    user=request.user,
                    order=order_g
                )
            else:
                instance = Payment.objects.create(
                    category=cat,
                    type_money=type_money,
                    price=price,
                    receipt=receipt,
                    user=request.user
                )

            return redirect('director:payments_list')
        return render(request, 'director/payment_create.html', context={'form': form})


from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group



@login_required(login_url='login')
def UserList(request):
    User = get_user_model()
    qs = User.objects.all()
    return render(request, 'director/user_list.html', context={'orders': qs})


@login_required(login_url='login')
def UserCreate(request):
    if request.method == 'POST':
        userName = request.POST.get('username', None)
        userPass = request.POST.get('password', None)
        userMail = request.POST.get('email', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        manager = request.POST.get('manager', None)
        designer = request.POST.get('designer', None)
        print(manager, designer)



        if userName and userPass and userMail:
            User = get_user_model()
            user = User.objects.create_user(username=userName,
                                            email=userMail,
                                            password=userPass,
                                            first_name=first_name,
                                            last_name=last_name)
            if manager == 'on':
                group = Group.objects.get(name='manager')
                group.user_set.add(user)
            if designer == 'on':
                group = Group.objects.get(name='designer')
                group.user_set.add(user)

            return redirect('director:order_view')

    return render(request, 'director/user_create.html')
