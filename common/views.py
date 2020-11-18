from django.shortcuts import render, redirect, HttpResponse
from orders.models import Customer, Payment, Order, Contract, Offer, OrderItemTextile1, OrderItemCornice, \
    OrderItemWorkSewing, OrderItemWorkAssembly, OrderItemWorkHanging, OrderItemWorkDelivery, PaymentCategory, Contract
from manager.models import SupplierOrderedTextile, SupplierOrderedCornice
from orders.forms import CustomerForm, PaymentForm
from materials.models import TextileManufact, CorniceManufact, Textile, Cornice, TextileCollection, CorniceCollection, \
    CorniceAdditional
from materials.forms import TextileManufactForm, CorniceManufactForm, TextileForm, CorniceForm, TextileCollectionForm, \
    CorniceCollectionForm, CorniceAdditionalForm
from works.models import Work, TypeWork
from works.forms import WorkForm
from markup.models import MarkupWorkCategory, MarkupCommon, MarkupMaterialCategory, MarkupSetting
from .utils import Get_Budget, GetStatusOrder, GetStatOrderPeriod, GetStatOrderFinishPeriod, GetCusPay
from django.contrib.auth.decorators import login_required



@login_required(login_url='login')
def CustomerList(request):
    qs = Customer.objects.all()

    return render(request, 'common/customers.html', context={'qs': qs})

@login_required(login_url='login')
def CustomerCreate(request):
    if request.method == 'GET':
        form = CustomerForm()
        return render(request, 'common/create_customer.html', context={'form': form})

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        source = request.POST.get("source", None)
        customer = request.POST.get("name", None)
        email = request.POST.get("email", None)
        phone = request.POST.get("phone", None)
        address = request.POST.get("address", None)
        pass_series = request.POST.get("pass_series", None)
        pass_number = request.POST.get("pass_number", None)
        pass_date = request.POST.get("pass_date", None)
        pass_issued = request.POST.get("pass_issued", None)

        if source != None and customer != None:
            instance = Customer.objects.create(
                name=customer,
                email=email,
                phone=phone,
                address=address,
                pass_series=pass_series,
                pass_number=pass_number,
                pass_date=pass_date,
                pass_issued=pass_issued
            )
            return redirect('common:customers_list')
    return render(request, 'common/create_customer.html', context={'form': form})

@login_required(login_url='login')
def PaymentsList(request):
    qs = Payment.objects.filter(user=request.user)
    return render(request, 'common/payments.html', context={'qs': qs})

@login_required(login_url='login')
def PaymentCreate(request):

    if request.method == 'GET':
        form = PaymentForm()
        return render(request, 'common/payment_create.html', context={'form': form})

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        category = request.POST.get("category", None)
        type_money = request.POST.get("type_money", None)
        price = request.POST.get("price", None)
        receipt = request.POST.get("receipt", None)

        if category != None and type_money !=None and price != None and receipt !=None:
            cat = PaymentCategory.objects.get(pk=category)
            instance = Payment.objects.create(
                category=cat,
                type_money=type_money,
                price=price,
                receipt=receipt,
                user=request.user
            )
            return redirect('common:payments_list')
        return render(request, 'main/payment_create.html', context={'form': form})

@login_required(login_url='login')
def WorksList(request):
    qs = Work.objects.all()
    markup = MarkupWorkCategory.objects.all()
    markup_c = MarkupCommon.objects.get(name='Общая')
    settings = MarkupSetting.objects.get(name='markup_view')
    return render(request, 'common/works_list.html', context={'qs': qs, 'markup': markup, 'markup_c': markup_c.markup, 'settings': settings})


@login_required(login_url='login')
def WorksAdd(request):
    if request.method == 'GET':
        form = WorkForm()
        return render(request, 'common/works_create.html', context={'form': form})

    if request.method == 'POST':
        form = TextileManufactForm(request.POST)
        name = request.POST.get("name", None)
        type_work = request.POST.get("type_work", None)
        price = request.POST.get("price", None)

        if name != None and type_work != None and price != None:
            type_w = TypeWork.objects.get(pk=type_work)
            instance = Work.objects.create(
                name=name,
                type_work=type_w,
                price=price
            )
            return redirect('common:works_list')
        return render(request, 'common/works_create.html', context={'form': form})

@login_required(login_url='login')
def WorksEdit(request, id):
    if request.method == 'GET':
        textile_m = Work.objects.get(pk=id)
        form = WorkForm({
            'name': textile_m.name,
            'type_work': textile_m.type_work,
            'price': textile_m.price})
        return render(request, 'common/works_edit.html', context={'form': form})

    if request.method == 'POST':
        form = WorkForm(request.POST)
        name = request.POST.get("name", None)
        type_work = request.POST.get("type_work", None)
        price = request.POST.get("price", None)

        if name != None and type_work != None and price != None:
            type_work_p = TypeWork.objects.get(pk=type_work)
            instance = Work.objects.get(pk=id)
            instance.name = name
            instance.type_work = type_work_p
            instance.price = price
            instance.save(update_fields=['name', 'type_work', 'price'])
            return redirect('common:works_list')
        return render(request, 'common/works_edit.html', context={'form': form})

@login_required(login_url='login')
def WorksRemove(request, id):
    qs = Work.objects.get(pk=id)
    qs.delete()
    return redirect('common:works_list')


@login_required(login_url='login')
def TextileManufactList(request):
    qs = TextileManufact.objects.all()
    qc = CorniceManufact.objects.all()
    result_list = sorted(
        chain(qs, qc),
        key=attrgetter('id'), reverse=True)
    return render(request, 'common/manufacturer_textile.html', context={'qs': result_list})


@login_required(login_url='login')
def TextileManufactAdd(request):
    if request.method == 'GET':
        form = TextileManufactForm()
        return render(request, 'common/manufacturer_create.html', context={'form': form})

    if request.method == 'POST':
        form = TextileManufactForm(request.POST)
        name = request.POST.get("name", None)
        email = request.POST.get("email", None)
        phone = request.POST.get("phone", None)
        manager = request.POST.get("manager", None)
        type_p = request.POST.get("type_p", None)

        if name != None and email != None:
            instance = TextileManufact.objects.create(
                name=name,
                email=email,
                phone=phone,
                manager=manager,
                type_p=type_p
            )
            return redirect('common:manufacturer_textile')
        return render(request, 'common/manufacturer_create.html', context={'form': form})

@login_required(login_url='login')
def TextileManufactEdit(request, id):
    if request.method == 'GET':
        textile_m = TextileManufact.objects.get(pk=id)
        form = TextileManufactForm({'name': textile_m.name,
                                    'type_p': textile_m.type_p,
                                    'email': textile_m.email,
                                    'phone': textile_m.phone,
                                    'manager': textile_m.manager})
        return render(request, 'common/manufacturer_edit.html', context={'form': form})

    if request.method == 'POST':
        form = TextileManufactForm(request.POST)
        name = request.POST.get("name", None)
        email = request.POST.get("email", None)
        phone = request.POST.get("phone", None)
        manager = request.POST.get("manager", None)
        type_p = request.POST.get("type_p", None)

        if name != None and email != None:
            instance = TextileManufact.objects.get(pk=id)
            instance.name = name
            instance.email = email
            instance.phone = phone
            instance.manager = manager
            instance.type_p = type_p
            instance.save(update_fields=['name', 'email', 'phone', 'manager', 'type_p'])
            return redirect('common:manufacturer_textile')
        return render(request, 'common/manufacturer_edit.html', context={'form': form})


@login_required(login_url='login')
def TextileManufactRemove(request, id):
    qs = TextileManufact.objects.get(pk=id)
    qs.delete()
    return redirect('common:manufacturer_textile')

@login_required(login_url='login')
def CorniceManufactAdd(request):
    if request.method == 'GET':
        form = CorniceManufactForm()
        return render(request, 'common/manufacturer_create.html', context={'form': form})

    if request.method == 'POST':
        form = CorniceManufactForm(request.POST)
        name = request.POST.get("name", None)
        email = request.POST.get("email", None)
        phone = request.POST.get("phone", None)
        manager = request.POST.get("manager", None)
        type_p = request.POST.get("type_p", None)

        if name != None and email != None:
            instance = CorniceManufact.objects.create(
                name=name,
                email=email,
                phone=phone,
                manager=manager,
                type_p=type_p
            )
            return redirect('common:manufacturer_textile')
        return render(request, 'common/manufacturer_create.html', context={'form': form})

@login_required(login_url='login')
def CorniceManufactEdit(request, id):
    if request.method == 'GET':
        textile_m = CorniceManufact.objects.get(pk=id)
        form = CorniceManufactForm({'name': textile_m.name,
                                    'type_p': textile_m.type_p,
                                    'email': textile_m.email,
                                    'phone': textile_m.phone,
                                    'manager': textile_m.manager})
        return render(request, 'common/manufacturer_edit.html', context={'form': form})

    if request.method == 'POST':
        form = CorniceManufactForm(request.POST)
        name = request.POST.get("name", None)
        email = request.POST.get("email", None)
        phone = request.POST.get("phone", None)
        manager = request.POST.get("manager", None)
        type_p = request.POST.get("type_p", None)

        if name != None and email != None:
            instance = CorniceManufact.objects.get(pk=id)
            instance.name = name
            instance.email = email
            instance.phone = phone
            instance.manager = manager
            instance.type_p = type_p
            instance.save(update_fields=['name', 'email', 'phone', 'manager', 'type_p'])
            return redirect('common:manufacturer_textile')
        return render(request, 'common/manufacturer_edit.html', context={'form': form})

@login_required(login_url='login')
def CorniceManufactRemove(request, id):
    qs = CorniceManufact.objects.get(pk=id)
    qs.delete()
    return redirect('common:manufacturer_textile')

@login_required(login_url='login')
def TextileList(request):
    qs = Textile.objects.all()[:100]
    collection = TextileCollection.objects.all()
    markup = MarkupMaterialCategory.objects.get(source_t=0)
    markup_c = MarkupCommon.objects.get(name='Общая')
    settings = MarkupSetting.objects.get(name='markup_view')
    print(settings.value)
    return render(request, 'common/textile_list.html', context={'qs': qs, 'markup': markup.markup, 'markup_c': markup_c.markup, 'collection': collection, 'settings': settings})

@login_required(login_url='login')
def TextileListFilter(request, collection_id, model_id):
    if collection_id != 'all':
        if model_id != 'all':
            m_id = model_id.replace('%20', ' ')
            get_collection = TextileCollection.objects.get(pk=collection_id)
            current_c = get_collection.name
            qs = Textile.objects.filter(collection=get_collection, model__icontains=m_id)
        else:
            get_collection = TextileCollection.objects.get(pk=collection_id)
            current_c = get_collection.name
            qs = Textile.objects.filter(collection=get_collection)
            m_id = 'all'
    else:
        qs = Textile.objects.all()[:100]
        current_c = 'all'
        m_id = 'all'

    current_m = m_id
    collection = TextileCollection.objects.all()
    if collection_id != 'all':
        get_collection = TextileCollection.objects.get(pk=collection_id)
        models = Textile.objects.filter(collection=get_collection).order_by().values('model').distinct()
    else:
        models = None
    
    markup = MarkupMaterialCategory.objects.get(source_t=0)
    markup_c = MarkupCommon.objects.get(name='Общая')
    settings = MarkupSetting.objects.get(name='markup_view')
    return render(request, 'common/textile_list.html', context={'qs': qs,
                                                                'current_c': current_c,
                                                                'current_m': current_m,
                                                                'markup': markup.markup,
                                                                'markup_c': markup_c.markup,
                                                                'collection': collection,
                                                                'models': models,
                                                                'settings': settings})


@login_required(login_url='login')
def TextileAdd(request):
    if request.method == 'GET':
        form = TextileForm()
        return render(request, 'common/textile_create.html', context={'form': form})

    if request.method == 'POST':
        form = TextileForm(request.POST)
        collection = request.POST.get("collection", None)
        model = request.POST.get("model", None)
        color = request.POST.get("color", None)
        height = request.POST.get("height", None)
        price_opt = request.POST.get("price_opt", None)


        if collection != None and model != None and price_opt != None:
            collection_obj = TextileCollection.objects.get(pk=collection)
            manufacturer_obj = collection_obj.manufacturer
            instance = Textile.objects.create(
                model=model,
                color=color,
                height=height,
                price_opt=price_opt,

            )
            instance.manufacturer = manufacturer_obj
            instance.collection = collection_obj
            instance.save()
            return redirect('common:textile_list')
        return render(request, 'common/textile_create.html', context={'form': form})

@login_required(login_url='login')
def TextileEdit(request, id):
    if request.method == 'GET':
        textile_id = Textile.objects.get(pk=id)
        form = TextileForm({'collection': textile_id.collection,
                            'model': textile_id.model,
                            'color': textile_id.color,
                            'height': textile_id.height,
                            'price_opt': textile_id.price_opt})
        return render(request, 'common/textile_edit.html', context={'form': form})

    if request.method == 'POST':
        form = TextileForm(request.POST)
        collection = request.POST.get("collection", None)
        model = request.POST.get("model", None)
        color = request.POST.get("color", None)
        height = request.POST.get("height", None)
        price_opt = request.POST.get("price_opt", None)

        if collection != None and model != None and price_opt != None:
            collection_g = TextileCollection.objects.get(pk=collection)
            instance = Textile.objects.get(pk=id)
            instance.collection = collection_g
            instance.model = model
            instance.color = color
            instance.height = height
            instance.price_opt = price_opt
            instance.save(update_fields=['model', 'color', 'height', 'price_opt'])
            return redirect('common:textile_filter', collection_id=collection_g.id, model_id=instance.model)
        return render(request, 'common/textile_edit.html', context={'form': form})


@login_required(login_url='login')
def TextileRemove(request, id):
    qs = Textile.objects.get(pk=id)
    qs.delete()
    return redirect('common:textile_list')


@login_required(login_url='login')
def CorniceList(request):
    qs = Cornice.objects.all()
    collection = CorniceCollection.objects.all()
    markup = MarkupMaterialCategory.objects.get(source_t=1)
    markup_c = MarkupCommon.objects.get(name='Общая')
    settings = MarkupSetting.objects.get(name='markup_view')
    return render(request, 'common/cornice_list.html', context={'qs': qs, 'markup': markup.markup, 'markup_c': markup_c.markup, 'collection': collection, 'settings': settings})

@login_required(login_url='login')
def CorniceAdd(request):
    if request.method == 'GET':
        form = CorniceForm()
        return render(request, 'common/cornice_create.html', context={'form': form})

    if request.method == 'POST':
        form = CorniceForm(request.POST)
        collection = request.POST.get("collection", None)
        model = request.POST.get("model", None)
        long = request.POST.get("long", None)
        price_opt = request.POST.get("price_opt", None)


        if collection != None and model != None and price_opt != None:
            collection_obj = CorniceCollection.objects.get(pk=collection)
            manufacturer_obj = collection_obj.manufacturer
            instance = Cornice.objects.create(
                model=model,
                long=long,
                price_opt=price_opt,
            )
            instance.manufacturer = manufacturer_obj
            instance.collection = collection_obj
            instance.save()
            return redirect('common:cornice_list')
        return render(request, 'common/cornice_create.html', context={'form': form})


@login_required(login_url='login')
def CorniceAdditionalView(request, id):
    if request.method == 'GET':
        cornice = Cornice.objects.get(pk=id)
        form = CorniceAdditionalForm({'cornice': cornice})
        return render(request, 'common/cornice_additional_create.html', context={'form': form, 'cornice': cornice})

    if request.method == 'POST':
        form = CorniceAdditionalForm(request.POST)
        cornice = request.POST.get("cornice", None)
        category = request.POST.get("category", None)
        name = request.POST.get("name", None)
        type_p = request.POST.get("type_p", None)
        price = request.POST.get("price", None)

        if cornice != None and name != None and price != None:
            cornice_g = Cornice.objects.get(pk=cornice)
            instance = CorniceAdditional.objects.create(
                cornice=cornice_g,
                category=category,
                name=name,
                type_p=type_p,
                price=price,
            )
            instance.save()
            return redirect('common:cornice_list')
        return render(request, 'common/cornice_additional_create.html', context={'form': form})

@login_required(login_url='login')
def CorniceAdditionalEdit(request, id):
    if request.method == 'GET':
        additional = CorniceAdditional.objects.get(pk=id)
        form = CorniceAdditionalForm({'category': additional.category, 'name': additional.name, 'type_p': additional.type_p, 'price': additional.price})
        return render(request, 'common/cornice_additional_edit.html', context={'form': form})

    if request.method == 'POST':
        form = CorniceAdditionalForm(request.POST)
        category = request.POST.get("category", None)
        name = request.POST.get("name", None)
        type_p = request.POST.get("type_p", None)
        price = request.POST.get("price", None)

        if name != None and price != None:
            instance = CorniceAdditional.objects.get(pk=id)
            instance.category = category
            instance.type_p = type_p
            instance.name = name
            instance.price = price
            instance.save(update_fields=['category', 'type_p', 'name', 'price'])
            return redirect('common:cornice_additional_list', id=instance.cornice.id)
        return render(request, 'common/cornice_additional_edit.html', context={'form': form})

@login_required(login_url='login')
def CorniceAdditionalDelete(request, id):
    additional = CorniceAdditional.objects.get(pk=id)
    cornice_d = additional.cornice
    additional.delete()
    return redirect('common:cornice_additional_list', id=cornice_d.id)

@login_required(login_url='login')
def CorniceAdditionalList(request, id):
    cornice_g = Cornice.objects.get(pk=id)
    additional = CorniceAdditional.objects.filter(cornice=cornice_g)
    return render(request, 'common/cornice_list_additional.html', context={'additional': additional, 'cornice': cornice_g})

def CorniceAdditionalOrder(request, id):
    cornice_g = Cornice.objects.get(pk=id)
    additional = CorniceAdditional.objects.filter(cornice=cornice_g)
    return render(request, 'common/cornice_list_additional.html', context={'additional': additional, 'cornice': cornice_g})

@login_required(login_url='login')
def CorniceEdit(request, id):
    if request.method == 'GET':
        textile_id = Cornice.objects.get(pk=id)
        additional = CorniceAdditional.objects.filter(cornice=textile_id)
        form = CorniceForm({'collection': textile_id.collection,
                            'model': textile_id.model,
                            'long': textile_id.long,
                            'price_opt': textile_id.price_opt})
        return render(request, 'common/cornice_edit.html', context={'form': form, 'cornice': textile_id, 'additional': additional})

    if request.method == 'POST':
        form = TextileForm(request.POST)
        collection = request.POST.get("collection", None)
        model = request.POST.get("model", None)
        long = request.POST.get("long", None)
        price_opt = request.POST.get("price_opt", None)

        if collection != None and model != None and price_opt != None:
            collection_g = CorniceCollection.objects.get(pk=collection)
            instance = Cornice.objects.get(pk=id)
            instance.collection = collection_g
            instance.model = model
            instance.long = long
            instance.price_opt = price_opt
            instance.save(update_fields=['collection', 'model', 'long', 'price_opt'])
            return redirect('common:cornice_list')
        return render(request, 'common/cornice_edit.html', context={'form': form})

@login_required(login_url='login')
def CorniceRemove(request, id):
    qs = Cornice.objects.get(pk=id)
    qs.delete()
    return redirect('common:cornice_list')

@login_required(login_url='login')
def TextileCollectionAdd(request):
    if request.method == 'GET':
        form = TextileCollectionForm()
        return render(request, 'common/collection_create.html', context={'form': form})

    if request.method == 'POST':
        form = TextileCollectionForm(request.POST)
        name = request.POST.get("name", None)
        manufacturer = request.POST.get("manufacturer", None)

        if name != None and manufacturer != None:
            manufacturer_obj = TextileManufact.objects.get(pk=manufacturer)
            instance = TextileCollection.objects.create(
                name=name
            )
            instance.manufacturer = manufacturer_obj
            instance.save()
            return redirect('common:textile_list')
        return render(request, 'common/collection_create.html', context={'form': form})


@login_required(login_url='login')
def CorniceCollectionAdd(request):
    if request.method == 'GET':
        form = CorniceCollectionForm()
        return render(request, 'common/collection_create.html', context={'form': form})

    if request.method == 'POST':
        form = CorniceCollectionForm(request.POST)
        name = request.POST.get("name", None)
        manufacturer = request.POST.get("manufacturer", None)

        if name != None and manufacturer != None:
            manufacturer_obj = CorniceManufact.objects.get(pk=manufacturer)
            instance = CorniceCollection.objects.create(
                name=name
            )
            instance.manufacturer = manufacturer_obj
            instance.save()
            return redirect('common:cornice_list')
        return render(request, 'common/collection_create.html', context={'form': form})

@login_required(login_url='login')
def ReportOrders(request):
    qs = Order.objects.filter(status__gte=5)
    customers = Customer.objects.all()
    budget_massive = {}
    for q in qs:
        budget_massive[q.id] = (Get_Budget(q.id))

    return render(request, 'common/report_orders.html', context={'orders': qs, 'budget': budget_massive, 'customers': customers})

import datetime
from django.db.models import Sum, Count
from django.utils import timezone


@login_required(login_url='login')
def dashboard_designer(request):
    customers = Customer.objects.filter(user=request.user).order_by('-date_created')[:8]
    payments = Payment.objects.filter(category__type_p=0, user=request.user).order_by('-date_created')[:7]

    end_n = datetime.datetime.now() + datetime.timedelta(days=1)
    end = end_n.strftime("%Y-%m-%d")
    end_s = end.split('-')
    start_n = end_n - datetime.timedelta(days=30)
    start = start_n.strftime("%Y-%m-%d")
    start_s = start.split('-')

    orders = Order.objects.filter(date_created__gte=start, date_created__lte=end)

    cus_cat_name = Customer._meta.get_field('source_t').choices
    cus_cat = Customer.objects.filter(date_created__gte=start, date_created__lte=end)
    cus_cat1 = cus_cat.values('source_t').annotate(Count('source_t')).order_by('source_t')

    cus_label = []
    cus_data = []
    for c in cus_cat1:
        data = c['source_t__count']
        cus_data.append(data)
        label = c['source_t']
        for cat in cus_cat_name:
            if label == cat[0]:
                cus_label.append(f"{cat[1]} - {data} шт.")

    f = GetStatOrderPeriod(start, end)
    g = GetStatOrderFinishPeriod(start, end)

    all_status = {
        '0': {
            'qs': GetStatusOrder(orders, 0),
            'name': 'ЗАПЛАНИРОВАН'
        },
        '1': {
            'qs': GetStatusOrder(orders, 1),
            'name': 'КП ПОДГОТОВЛЕНО'
        },
        '2': {
            'qs': GetStatusOrder(orders, 2),
            'name': 'КП УТВЕРЖДЕНО'
        },
        '3': {
            'qs': GetStatusOrder(orders, 3),
            'name': 'Договор подготовлен'
        },
        '4': {
            'qs': GetStatusOrder(orders, 4),
            'name': 'Договор подписан'
        },
        '5': {
            'qs': GetStatusOrder(orders, 5),
            'name': 'Аванс получен'
        },

    }
    period = str(start_n.strftime("%d.%m.%Y")) + ' - ' + str(end_n.strftime("%d.%m.%Y"))

    return render(request, 'common/dashboard_designer.html', context={'orders':     all_status,
                                                                      'customers':  customers,
                                                                      'payments':   payments,
                                                                      'cus_label':  cus_label,
                                                                      'cus_data':   cus_data,
                                                                      'data1': f[0],
                                                                      'qs_count1': f[1],
                                                                      'data2': g[0],
                                                                      'qs_count2': g[1],
                                                                      'startDate': [int(start_s[0]),
                                                                                    int(start_s[1]) - 1,
                                                                                    int(start_s[2])],
                                                                      'endDate': [int(end_s[0]), int(end_s[1]) - 1,
                                                                                  int(end_s[2])],
                                                                      'period': period
                                                                      })

@login_required(login_url='login')
def dashboard_designer_date(request, start, end):


    start_s = start.split('-')
    start = datetime.date(int(start_s[0]), int(start_s[1]), int(start_s[2]))
    end_s = end.split('-')
    end = datetime.date(int(end_s[0]), int(end_s[1]), int(end_s[2])) + datetime.timedelta(days=1)
    orders = Order.objects.filter(date_created__gte=start, date_created__lte=end)
    customers = Customer.objects.filter(user=request.user).order_by('-date_created')[:8]
    payments = Payment.objects.filter(category__type_p=0, user=request.user).order_by('-date_created')[:7]

    f = GetStatOrderPeriod(start, end)
    g = GetStatOrderFinishPeriod(start, end)

    all_status = {
        '0': {
            'qs': GetStatusOrder(orders, 0),
            'name': 'ЗАПЛАНИРОВАН'
        },
        '1': {
            'qs': GetStatusOrder(orders, 1),
            'name': 'КП ПОДГОТОВЛЕНО'
        },
        '2': {
            'qs': GetStatusOrder(orders, 2),
            'name': 'КП УТВЕРЖДЕНО'
        },
        '3': {
            'qs': GetStatusOrder(orders, 3),
            'name': 'Договор подготовлен'
        },
        '4': {
            'qs': GetStatusOrder(orders, 4),
            'name': 'Договор подписан'
        },
        '5': {
            'qs': GetStatusOrder(orders, 5),
            'name': 'Аванс получен'
        },

    }
    period = str(start.strftime("%d.%m.%Y")) + ' - ' + str(end.strftime("%d.%m.%Y"))

    return render(request, 'common/dashboard_designer.html', context={'orders': all_status,
                                                                      'period': period,
                                                                      'customers': customers,
                                                                      'payments': payments,
                                                                      'data1': f[0],
                                                                      'qs_count1': f[1],
                                                                      'data2': g[0],
                                                                      'qs_count2': g[1],
                                                                      'startDate': [int(start_s[0]), int(start_s[1])-1, int(start_s[2])],
                                                                      'endDate':   [int(end_s[0]), int(end_s[1])-1, int(end_s[2])],
                                                                      })

from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear
from itertools import chain
from operator import attrgetter

@login_required(login_url='login')
def dashboard_manager(request):

    customers = Customer.objects.all().order_by('-id')[:8]
    payments = Payment.objects.filter(category__type_p=0).order_by('-date_created')[:7]

    end_n = datetime.datetime.now() + datetime.timedelta(days=1)
    end = end_n.strftime("%Y-%m-%d")
    end_s = end.split('-')
    start_n = end_n - datetime.timedelta(days=30)
    start = start_n.strftime("%Y-%m-%d")
    start_s = start.split('-')

    qs = SupplierOrderedTextile.objects.filter(date_created__gte=start, date_created__lte=end)
    qc = SupplierOrderedCornice.objects.filter(date_created__gte=start, date_created__lte=end)
    result_list = sorted(
        chain(qs, qc),
        key=attrgetter('date_created'), reverse=True)

    orders = Order.objects.filter(date_created__gte=start, date_created__lte=end)

    cus_cat_name = Customer._meta.get_field('source_t').choices
    cus_cat = Customer.objects.filter(date_created__gte=start, date_created__lte=end)
    cus_cat1 = cus_cat.values('source_t').annotate(Count('source_t')).order_by('source_t')

    cus_label = []
    cus_data = []
    for c in cus_cat1:
        data = c['source_t__count']
        cus_data.append(data)
        label = c['source_t']
        for cat in cus_cat_name:
            if label == cat[0]:
                cus_label.append(f"{cat[1]} - {data} шт.")


    all_status = {
        '5': {
            'qs': GetStatusOrder(orders, 5),
            'name': 'Аванс получен'
        },
        '6': {
            'qs': GetStatusOrder(orders, 6),
            'name': 'Материалы заказаны'
        },
        '7': {
            'qs': GetStatusOrder(orders, 7),
            'name': 'Материалы оплачены'
        },
        '8': {
            'qs': GetStatusOrder(orders, 8),
            'name': 'Материалы отгружены'
        },
        '9': {
            'qs': GetStatusOrder(orders, 9),
            'name': 'Работы заказаны'
        },


    }
    period = str(start_n.strftime("%d.%m.%Y")) + ' - ' + str(end_n.strftime("%d.%m.%Y"))

    budget_mass = {}

    for q in orders.filter(status=10).order_by('date_finished'):
        contract = Contract.objects.get(order=q)
        payment = Payment.objects.filter(order=q, category__type_p=1).aggregate(Sum('price'))
        name = contract.order.number
        profit = float(contract.price) - float(payment['price__sum'])
        marga = profit * 100 / float(contract.price)
        budget_mass[name] = {
            'arrival': contract.price,
            'expense': payment['price__sum'],
            'profit': round(profit, 2),
            'marga': round(marga, 2)
        }

    qs111 = orders.filter(status=10).annotate(
        day=ExtractDay('date_finished')).annotate(month=ExtractMonth('date_finished')).\
        annotate(year=ExtractYear('date_finished')).values('day', 'month', 'year'
    ).annotate(
        n=Count('pk')
    ).order_by('day')

    date_finish = []
    for q in qs111:
        year = q['year']
        month = q['month']
        day = q['day']
        date_finish.append(datetime.date(year, month, day))

    date2_mass = []
    arrival_mass = []
    expense_mass = []
    profit_mass = []

    y = 0
    for d in date_finish:
        orders777 = Order.objects.filter(date_finished=d)

        summ_arrival = 0
        summ_expense = 0
        summ_profit = 0

        for q in orders777:
            contract = Contract.objects.get(order=q)
            payment = Payment.objects.filter(order=q, category__type_p=0).aggregate(Sum('price'))
            arrival = contract.price
            expense = payment['price__sum']
            profit = float(contract.price) - float(payment['price__sum'])
            summ_arrival += arrival
            summ_expense += expense
            summ_profit += profit

        arrival_mass.append([y, summ_arrival])
        expense_mass.append([y, summ_expense])
        profit_mass.append([y, summ_profit])
        date2_mass.append([y, d.strftime("%d.%m")])
        y += 1

    max_mass = []
    for m in arrival_mass:
        max_mass.append(m[1])

    summ_budget_period = {}

    value_a = 0
    for a in arrival_mass:
        value_a += a[1]
    summ_budget_period['arrival'] = round(value_a, 2)
    value_e = 0
    for a in expense_mass:
        value_e += a[1]
    summ_budget_period['expense'] = round(value_e, 2)
    value_p = 0
    for a in profit_mass:
        value_p += a[1]
    summ_budget_period['profit'] = round(value_p, 2)
    print(summ_budget_period)


    cus_pay_order = orders.filter(status__gte=5).order_by('-pk')[:7]
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
    print(cus_pay_dic)



    return render(request, 'common/dashboard_manager.html', context={'orders':     all_status,
                                                                     'qs': result_list[:15],
                                                                     'order_test': cus_pay_dic,
                                                                     'budget': budget_mass,
                                                                     'budget_fin': summ_budget_period,
                                                                     'budget_order': orders.filter(status=10).order_by('-pk')[:6],
                                                                      'customers':  customers,
                                                                      'payments':   payments,
                                                                      'cus_label':  cus_label,
                                                                      'cus_data':   cus_data,
                                                                      'startDate': [int(start_s[0]),
                                                                                    int(start_s[1]) - 1,
                                                                                    int(start_s[2])],
                                                                      'endDate': [int(end_s[0]), int(end_s[1]) - 1,
                                                                                  int(end_s[2])],
                                                                     'period': period,
                                                                     'date_mass': date2_mass,
                                                                     'arrival_mass': arrival_mass,
                                                                     'expense_mass': expense_mass,
                                                                     'profit_mass': profit_mass,
                                                                     'max': max(max_mass)+4500})

@login_required(login_url='login')
def dashboard_manager_date(request, start, end):

    customers = Customer.objects.all().order_by('-id')[:7]
    payments = Payment.objects.filter(category__type_p=0).order_by('-date_created')[:7]

    start_s = start.split('-')
    start1 = datetime.date(int(start_s[0]), int(start_s[1]), int(start_s[2]))
    end_s = end.split('-')
    end1 = datetime.date(int(end_s[0]), int(end_s[1]), int(end_s[2])) + datetime.timedelta(days=1)

    qs = SupplierOrderedTextile.objects.filter(date_created__gte=start1, date_created__lte=end1).order_by('-pk')[:15]
    orders = Order.objects.filter(date_created__gte=start1, date_created__lte=end1)

    cus_cat_name = Customer._meta.get_field('source_t').choices
    cus_cat = Customer.objects.filter(date_created__gte=start1, date_created__lte=end1)
    cus_cat1 = cus_cat.values('source_t').annotate(Count('source_t')).order_by('source_t')

    cus_label = []
    cus_data = []
    for c in cus_cat1:
        data = c['source_t__count']
        cus_data.append(data)
        label = c['source_t']
        for cat in cus_cat_name:
            if label == cat[0]:
                cus_label.append(f"{cat[1]} - {data} шт.")

    f = GetStatOrderPeriod(start, end)
    g = GetStatOrderFinishPeriod(start, end)

    all_status = {
        '5': {
            'qs': GetStatusOrder(orders, 5),
            'name': 'Аванс получен'
        },
        '6': {
            'qs': GetStatusOrder(orders, 6),
            'name': 'Материалы заказаны'
        },
        '7': {
            'qs': GetStatusOrder(orders, 7),
            'name': 'Материалы оплачены'
        },
        '8': {
            'qs': GetStatusOrder(orders, 8),
            'name': 'Материалы отгружены'
        },
        '9': {
            'qs': GetStatusOrder(orders, 9),
            'name': 'Работы заказаны'
        },


    }
    period = str(start1.strftime("%d.%m.%Y")) + ' - ' + str(end1.strftime("%d.%m.%Y"))

    budget_mass = {}

    for q in orders.filter(status=10).order_by('date_finished'):
        contract = Contract.objects.get(order=q)
        payment = Payment.objects.filter(order=q).aggregate(Sum('price'))
        name = contract.order.number
        profit = float(contract.price) - float(payment['price__sum'])
        marga = profit * 100 / float(contract.price)
        budget_mass[name] = {
            'arrival': contract.price,
            'expense': payment['price__sum'],
            'profit': round(profit, 2),
            'marga': round(marga, 2)
        }

    qs111 = orders.filter(status=10).annotate(
        day=ExtractDay('date_finished')).annotate(month=ExtractMonth('date_finished')).\
        annotate(year=ExtractYear('date_finished')).values('day', 'month', 'year'
    ).annotate(
        n=Count('pk')
    ).order_by('day')

    date_finish = []
    for q in qs111:
        year = q['year']
        month = q['month']
        day = q['day']
        date_finish.append(datetime.date(year, month, day))

    date2_mass = []
    arrival_mass = []
    expense_mass = []
    profit_mass = []

    y = 0
    for d in date_finish:
        orders777 = Order.objects.filter(date_finished=d)

        summ_arrival = 0
        summ_expense = 0
        summ_profit = 0

        for q in orders777:
            contract = Contract.objects.get(order=q)
            payment = Payment.objects.filter(order=q).aggregate(Sum('price'))
            arrival = contract.price
            expense = payment['price__sum']
            profit = float(contract.price) - float(payment['price__sum'])
            summ_arrival += arrival
            summ_expense += expense
            summ_profit += profit

        arrival_mass.append([y, summ_arrival])
        expense_mass.append([y, summ_expense])
        profit_mass.append([y, summ_profit])
        date2_mass.append([y, d.strftime("%d.%m")])
        y += 1

    max_mass = []
    if len(arrival_mass) > 0:
        for m in arrival_mass:
            max_mass.append(m[1])
        max_value = max(max_mass)+4500
    else:
        max_value = 10000

    summ_budget_period = {}

    value_a = 0
    for a in arrival_mass:
        value_a += a[1]
    summ_budget_period['arrival'] = round(value_a, 2)
    value_e = 0
    for a in expense_mass:
        value_e += a[1]
    summ_budget_period['expense'] = round(value_e, 2)
    value_p = 0
    for a in profit_mass:
        value_p += a[1]
    summ_budget_period['profit'] = round(value_p, 2)
    return render(request, 'common/dashboard_manager.html', context={'orders':     all_status,
                                                                     'qs': qs,
                                                                     'budget': budget_mass,
                                                                     'budget_fin': summ_budget_period,
                                                                     'budget_order': orders.filter(status=10).order_by('-pk')[:6],
                                                                      'customers':  customers,
                                                                      'payments':   payments,
                                                                      'cus_label':  cus_label,
                                                                      'cus_data':   cus_data,
                                                                      'data1': f[0],
                                                                      'qs_count1': f[1],
                                                                      'data2': g[0],
                                                                      'qs_count2': g[1],
                                                                      'startDate': [int(start_s[0]),
                                                                                    int(start_s[1]) - 1,
                                                                                    int(start_s[2])],
                                                                      'endDate': [int(end_s[0]), int(end_s[1]) - 1,
                                                                                  int(end_s[2])],
                                                                     'period': period,
                                                                     'date_mass': date2_mass,
                                                                     'arrival_mass': arrival_mass,
                                                                     'expense_mass': expense_mass,
                                                                     'profit_mass': profit_mass,
                                                                     'max': max_value})