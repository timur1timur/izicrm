from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse

from orders.models import Customer, Payment, Order, Contract, Offer, OrderItemTextile1, OrderItemCornice, \
    OrderItemWorkSewing, OrderItemWorkAssembly, OrderItemWorkHanging, OrderItemWorkDelivery, PaymentCategory, Contract
from manager.models import SupplierOrderedTextile, SupplierOrderedCornice
from orders.forms import CustomerForm, PaymentForm, CustomerEditForm, PaymentCategoryForm
from materials.models import TextileManufact, CorniceManufact, Textile, Cornice, TextileCollection, CorniceCollection, \
    CorniceAdditional, CorniceCollectionColor, CorniceAdditionalOptions
from materials.forms import TextileManufactForm, CorniceManufactForm, TextileForm, CorniceForm, TextileCollectionForm, \
    CorniceCollectionForm, CorniceAdditionalForm, CorniceCollectionColorForm, CorniceAdditionalOptionsForm
from works.models import Work, TypeWork
from works.forms import WorkForm
from markup.models import MarkupWorkCategory, MarkupCommon, MarkupMaterialCategory, MarkupSetting, MarkupCustomerCategory
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
def CustomerEdit(request, id):
    if request.method == 'GET':
        cus = Customer.objects.get(pk=id)
        form = CustomerEditForm({
            'name': cus.name,
            'phone': cus.phone,
            'email': cus.email,
            'address': cus.address,
            'pass_series': cus.pass_series,
            'pass_number': cus.pass_number,
            'pass_date': cus.pass_date,
            'pass_issued': cus.pass_issued,
            'source_t': cus.source_t
        })
        return render(request, 'common/edit_customer.html', context={'form': form})

    if request.method == 'POST':
        form = CustomerEditForm(request.POST)
        source_t = request.POST.get("source_t", None)
        name = request.POST.get("name", None)
        email = request.POST.get("email", None)
        phone = request.POST.get("phone", None)
        address = request.POST.get("address", None)
        pass_series = request.POST.get("pass_series", None)
        pass_number = request.POST.get("pass_number", None)
        pass_date = request.POST.get("pass_date", None)
        pass_issued = request.POST.get("pass_issued", None)

        if source_t != None and name != None:
            instance = Customer.objects.get(pk=id)
            instance.name = name
            instance.email = email
            instance.phone = phone
            instance.address = address
            instance.pass_series = pass_series
            instance.pass_number = pass_number
            instance.pass_date = pass_date
            instance.pass_issued = pass_issued
            instance.source_t = source_t
            instance.save(update_fields=['name', 'email', 'phone', 'address', 'pass_series', 'pass_number', 'pass_date', 'pass_issued', 'source_t'])
            return redirect('common:customers_list')
    return render(request, 'common/edit_customer.html', context={'form': form})

@login_required(login_url='login')
def PaymentsList(request):
    qs = Payment.objects.filter(user=request.user)
    return render(request, 'common/payments.html', context={'qs': qs})



@login_required(login_url='login')
def PaymentCategoryCreate(request):

    if request.method == 'GET':
        form = PaymentCategoryForm()
        return render(request, 'common/payment_category_create.html', context={'form': form})

    if request.method == 'POST':
        form = PaymentCategoryForm(request.POST)
        name = request.POST.get("name", None)
        type_p = request.POST.get("type_p", None)

        if name != None and type_p !=None:
            instance = PaymentCategory.objects.create(
                name=name,
                type_p=type_p,

            )
            return redirect('director:payments_list')
        return render(request, 'main/payment_category_create.html', context={'form': form})


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


def test_textile(request):
    return render(request, 'common/textile_l.html')


def search_textile(request, q):
    if TextileCollection.objects.filter(name__icontains=q).exists():
        qs_collection = TextileCollection.objects.filter(name__icontains=q)
    else:
        qs_collection = 0

    if Textile.objects.filter(model__icontains=q).exists():
        qs_model = Textile.objects.filter(model__icontains=q)
    else:
        qs_model = 0

    if Textile.objects.filter(article__icontains=q).exists():
        qs_article = Textile.objects.filter(article__icontains=q)
    else:
        qs_article = 0
    # return JsonResponse({'data_c': qs_collection,
    #                      'data_m': qs_textile,
    #                      'data_a': qs_article
    #                      })
    return render(request, 'common/textile_search.html', context={'qs_m': qs_model,
                                                                  'qs_a': qs_article,
                                                                  'qs_c': qs_collection,
                                                                  })


def get_json_collection(request):
    qs = list(TextileCollection.objects.values().order_by('name'))
    return JsonResponse({'data': qs})



def get_markup_customer(request):
    qs = list(MarkupCustomerCategory.objects.values())
    return JsonResponse({'data': qs})


def set_markup_customer(request):
    if request.is_ajax:
        set_m = MarkupSetting.objects.get(name='markup_customer')
        get_val = request.GET.get('customer')
        set_m.value = get_val
        set_m.save(update_fields=['value'])
        return JsonResponse({'data': True})
    return JsonResponse({'data': False})


def get_json_models(request):
    selected_collection = request.GET.get('collection')
    obj = TextileCollection.objects.get(pk=selected_collection)
    qs = list(Textile.objects.filter(collection=obj).order_by().values('model').distinct())
    return JsonResponse({'data': qs})

from django.utils.safestring import mark_safe

def get_json_qs(request):
    if request.is_ajax:
        collection = request.GET.get('collection')
        collection_g = TextileCollection.objects.get(pk=collection)
        model = request.GET.get('model')
        if model == 'all':
            model_g = list(Textile.objects.filter(collection=collection_g).values())
        else:
            model_g = list(Textile.objects.filter(collection=collection_g, model__icontains=model).values())

        mass = []
        for item in model_g:
            ff = '<a href="%s" title="" data-toggle="tooltip" data-original-title="Изменить">%s</a>' % (f"edit/{item['id']}/", '<i data-feather="edit-3" class="wd-16 mr-2"></i>')
            item['link'] = ff
            mass.append(item)
        print(mass)
        return JsonResponse({'data': mass})
    return JsonResponse({'data': False})






@login_required(login_url='login')
def TextileListFilter(request, collection_id, model_id):
    if collection_id != 'all':
        if model_id != 'all':
            m_id = model_id.replace('%20', ' ')
            get_collection = TextileCollection.objects.get(pk=collection_id)
            current_c = get_collection.id
            qs = Textile.objects.filter(collection=get_collection, model__icontains=m_id)
        else:
            get_collection = TextileCollection.objects.get(pk=collection_id)
            current_c = get_collection.id
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
    get_m = MarkupSetting.objects.get(name='markup_customer')
    markup_cus = MarkupCustomerCategory.objects.get(source_t=get_m.value)
    markup = MarkupMaterialCategory.objects.get(source_t=0)
    markup_c = MarkupCommon.objects.get(name='Общая')
    markup_common = markup_c.markup * markup_cus.markup * markup.markup
    print(markup_common)
    markup_storage = markup_c.markup * markup_cus.markup
    print(f'Markup storage: {markup_storage}')
    settings = MarkupSetting.objects.get(name='markup_view')
    return render(request, 'common/textile_list.html', context={'qs': qs,
                                                                'current_c': current_c,
                                                                'current_m': current_m,
                                                                'markup': markup.markup,
                                                                'markup_c': markup_c.markup,
                                                                'markup_cus': markup_cus.markup,
                                                                'markup_common': markup_common,
                                                                'markup_storage': markup_storage,
                                                                'get_m': get_m,
                                                                'collection': collection,
                                                                'models': models,
                                                                'settings': settings})


from materials.utils import transliterate

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
        currency = request.POST.get("currency", None)


        if collection != None and model != None and price_opt != None:
            collection_obj = TextileCollection.objects.get(pk=collection)
            manufacturer_obj = collection_obj.manufacturer
            instance = Textile.objects.create(
                
                model=model,
                color=color,
                height=height,
                price_opt=price_opt,
                currency=currency

            )
            instance.manufacturer = manufacturer_obj
            instance.collection = collection_obj
            instance.save()
            obj = Textile.objects.get(pk=instance.pk)
            obj.article = transliterate(str(obj.collection.name)[0]).upper() + transliterate(str(obj.model)[0]).upper()[0] + str(obj.pk)
            obj.save(update_fields=['article'])

            return redirect('common:textile_filter', collection_id=collection_obj.id, model_id='all')
        return render(request, 'common/textile_create.html', context={'form': form})

@login_required(login_url='login')
def TextileEdit(request, id):
    if request.method == 'GET':
        textile_id = Textile.objects.get(pk=id)
        form = TextileForm({'collection': textile_id.collection,
                            'model': textile_id.model,
                            'color': textile_id.color,
                            'height': textile_id.height,
                            'currency': textile_id.currency,
                            'price_opt': textile_id.price_opt,
                            'article': textile_id.article})
        return render(request, 'common/textile_edit.html', context={'form': form})

    if request.method == 'POST':
        form = TextileForm(request.POST)
        collection = request.POST.get("collection", None)
        model = request.POST.get("model", None)
        color = request.POST.get("color", None)
        height = request.POST.get("height", None)
        price_opt = request.POST.get("price_opt", None)
        article = request.POST.get("article", None)
        currency = request.POST.get("currency", None)


        if collection != None and model != None and price_opt != None:
            collection_g = TextileCollection.objects.get(pk=collection)
            instance = Textile.objects.get(pk=id)
            instance.collection = collection_g
            instance.model = model
            instance.color = color
            instance.height = height
            instance.price_opt = price_opt
            instance.article = article
            instance.currency = currency

            instance.save(update_fields=['model', 'color', 'height', 'price_opt', 'article', 'currency'])
            return redirect('common:textile_filter', collection_id=collection_g.id, model_id='all')
        return render(request, 'common/textile_edit.html', context={'form': form})


@login_required(login_url='login')
def TextileRemove(request, id):
    qs_callback = Textile.objects.get(pk=id)
    qs = Textile.objects.get(pk=id)
    qs.delete()
    return redirect('common:textile_filter', collection_id=qs_callback.collection.id, model_id='all')


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
def CorniceAdditionalList(request):
    additional = CorniceAdditional.objects.all()
    collection = CorniceCollection.objects.all()
    return render(request, 'common/cornice_additional_list.html', context={'additional': additional, 'collection': collection})

@login_required(login_url='login')
def CorniceAdditionalAdd(request):
    if request.method == 'GET':
        form = CorniceAdditionalForm()
        return render(request, 'common/cornice_additional_create.html', context={'form': form})

    if request.method == 'POST':
        form = CorniceAdditionalForm(request.POST)
        collection = request.POST.get("collection", None)
        category = request.POST.get("category", None)
        name = request.POST.get("name", None)

        if collection != None and name != None and category != None:
            collection_g = CorniceCollection.objects.get(pk=collection)
            instance = CorniceAdditional.objects.create(
                collection=collection_g,
                category=category,
                name=name
            )
            instance.save()
            return redirect('common:cornice_additional_list')
        return render(request, 'common/cornice_additional_create.html', context={'form': form})

@login_required(login_url='login')
def CorniceAdditionalEdit(request, id):
    if request.method == 'GET':
        additional = CorniceAdditional.objects.get(pk=id)
        form = CorniceAdditionalForm({'category': additional.category, 'name': additional.name})
        return render(request, 'common/cornice_additional_edit.html', context={'form': form, 'collection': additional.collection.name})

    if request.method == 'POST':
        form = CorniceAdditionalForm(request.POST)
        category = request.POST.get("category", None)
        name = request.POST.get("name", None)

        if name != None and category != None:
            instance = CorniceAdditional.objects.get(pk=id)
            instance.category = category
            instance.name = name
            instance.save(update_fields=['category', 'name'])
            return redirect('common:cornice_additional_list')
        return render(request, 'common/cornice_additional_edit.html', context={'form': form})

@login_required(login_url='login')
def CorniceAdditionalDelete(request, id):
    additional = CorniceAdditional.objects.get(pk=id)
    additional.delete()
    return redirect('common:cornice_additional_list')

@login_required(login_url='login')
def CorniceAdditionalOrder(request, id):
    cornice_g = Cornice.objects.get(pk=id)
    additional = CorniceAdditional.objects.filter(cornice=cornice_g)
    return render(request, 'common/cornice_list_additional.html', context={'additional': additional, 'cornice': cornice_g})


@login_required(login_url='login')
def CorniceAdditionalOptionsList(request, id):
    additional = CorniceAdditional.objects.get(pk=id)
    options = CorniceAdditionalOptions.objects.filter(additional=additional)
    return render(request, 'common/cornice_additional_options_list.html', context={'additional': additional, 'options': options})

@login_required(login_url='login')
def CorniceAdditionalOptionsAdd(request, id):
    if request.method == 'GET':
        additional = CorniceAdditional.objects.get(pk=id)
        form = CorniceAdditionalOptionsForm()
        return render(request, 'common/cornice_additional_options_create.html', context={'form': form, 'additional': additional})

    if request.method == 'POST':
        form = CorniceAdditionalOptionsForm(request.POST)
        type_p = request.POST.get("type_p", None)
        price = request.POST.get("price", None)

        if type_p != None and price != None:
            additional_g = CorniceAdditional.objects.get(pk=id)
            instance = CorniceAdditionalOptions.objects.create(
                additional=additional_g,
                type_p=type_p,
                price=price
            )
            instance.save()
            return redirect('common:cornice_additional_options_list', id=additional_g.id)
        return render(request, 'common/cornice_additional_options_create.html', context={'form': form})

@login_required(login_url='login')
def CorniceAdditionalOptionsEdit(request, id):
    if request.method == 'GET':
        options = CorniceAdditionalOptions.objects.get(pk=id)
        form = CorniceAdditionalOptionsForm({'additional': options.additional, 'type_p': options.type_p, 'price': options.price})
        return render(request, 'common/cornice_additional_options_edit.html', context={'form': form, 'options': options})

    if request.method == 'POST':
        form = CorniceAdditionalOptionsForm(request.POST)
        type_p = request.POST.get("type_p", None)
        price = request.POST.get("price", None)

        if type_p != None and price != None:
            instance = CorniceAdditionalOptions.objects.get(pk=id)
            instance.type_p = type_p
            instance.price = price
            instance.save(update_fields=['type_p', 'price'])
            instance.save()
            return redirect('common:cornice_additional_options_list', id=instance.additional.id)
        return render(request, 'common/cornice_additional_options_create.html', context={'form': form})

@login_required(login_url='login')
def CorniceAdditionalOptionsRemove(request, id):
     options = CorniceAdditionalOptions.objects.get(pk=id)
     additional = options.additional
     options.delete()
     return redirect('common:cornice_additional_options_list', id=additional.id)

@login_required(login_url='login')
def CorniceEdit(request, id):
    if request.method == 'GET':
        textile_id = Cornice.objects.get(pk=id)
        form = CorniceForm({'collection': textile_id.collection,
                            'model': textile_id.model,
                            'long': textile_id.long,
                            'price_opt': textile_id.price_opt})
        return render(request, 'common/cornice_edit.html', context={'form': form, 'cornice': textile_id})

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
def TextileCollectionList(request):
    collection = TextileCollection.objects.all()
    manufactor = TextileManufact.objects.all()
    return render(request, 'common/textile_collection_list.html', context={'collection': collection, 'manufactor': manufactor})



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
            return redirect('common:collection_textile_list')
        return render(request, 'common/collection_create.html', context={'form': form})

@login_required(login_url='login')
def TextileCollectionEdit(request, id):
    if request.method == 'GET':
        textile_collection = TextileCollection.objects.get(pk=id)
        form = TextileCollectionForm({'name': textile_collection.name, 'manufacturer': textile_collection.manufacturer})
        return render(request, 'common/collection_edit.html', context={'form': form, 'collection': textile_collection.name})

    if request.method == 'POST':
        form = TextileCollectionForm(request.POST)
        name = request.POST.get("name", None)
        manufacturer = request.POST.get("manufacturer", None)

        if name != None and manufacturer != None:
            manufacturer_obj = TextileManufact.objects.get(pk=manufacturer)
            instance = TextileCollection.objects.get(pk=id)
            instance.name = name
            instance.manufacturer = manufacturer_obj
            instance.save(update_fields=['name', 'manufacturer'])
            return redirect('common:collection_textile_list')
        return render(request, 'common/collection_edit.html', context={'form': form})

@login_required(login_url='login')
def TextileCollectionRemove(request, id):
    obj = TextileCollection.objects.get(pk=id)
    obj.delete()
    return redirect('common:collection_textile_list')


@login_required(login_url='login')
def CorniceCollectionList(request):
    collection = CorniceCollection.objects.all()
    manufactor = CorniceManufact.objects.all()
    return render(request, 'common/cornice_collection_list.html', context={'collection': collection, 'manufactor': manufactor})

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
            return redirect('common:collection_cornice_list')
        return render(request, 'common/collection_create.html', context={'form': form})

@login_required(login_url='login')
def CorniceCollectionEdit(request, id):
    if request.method == 'GET':
        cornice_collection = CorniceCollection.objects.get(pk=id)
        form = CorniceCollectionForm({'name': cornice_collection.name, 'manufacturer': cornice_collection.manufacturer})
        return render(request, 'common/collection_edit.html', context={'form': form, 'collection': cornice_collection.name})

    if request.method == 'POST':
        form = CorniceCollectionForm(request.POST)
        name = request.POST.get("name", None)
        manufacturer = request.POST.get("manufacturer", None)

        if name != None and manufacturer != None:
            manufacturer_obj = CorniceManufact.objects.get(pk=manufacturer)
            instance = CorniceCollection.objects.get(pk=id)
            instance.manufacturer = manufacturer_obj
            instance.name = name
            instance.save(update_fields=['name', 'manufacturer'])
            return redirect('common:collection_cornice_list')
        return render(request, 'common/collection_edit.html', context={'form': form})

@login_required(login_url='login')
def CorniceCollectionRemove(request, id):
    obj = CorniceCollection.objects.get(pk=id)
    obj.delete()
    return redirect('common:collection_cornice_list')


@login_required(login_url='login')
def CorniceCollectionColorAdd(request, id):
    if request.method == 'GET':
        collection = CorniceCollection.objects.get(pk=id)
        form = CorniceCollectionColorForm()
        return render(request, 'common/collection_color_create.html', context={'form': form, 'collection': collection})

    if request.method == 'POST':
        form = CorniceCollectionForm(request.POST)
        color = request.POST.get("color", None)

        if color != None:
            collection_obj = CorniceCollection.objects.get(pk=id)
            instance = CorniceCollectionColor.objects.create(
                color=color
            )
            collection_obj.color.add(instance)
            return redirect('common:collection_cornice_list')
        return render(request, 'common/collection_color_create.html', context={'form': form})


@login_required(login_url='login')
def CorniceCollectionColorEdit(request, id, color_id):
    if request.method == 'GET':
        collection = CorniceCollection.objects.get(pk=id)
        color = CorniceCollectionColor.objects.get(pk=color_id)
        form = CorniceCollectionColorForm({'color': color.color})
        return render(request, 'common/collection_color_edit.html', context={'form': form, 'collection': collection})

    if request.method == 'POST':
        form = CorniceCollectionForm(request.POST)
        color = request.POST.get("color", None)

        if color != None:
            collection_obj = CorniceCollection.objects.get(pk=id)
            instance = CorniceCollectionColor.objects.get(pk=color_id)
            instance.color = color
            instance.save(update_fields=['color'])
            return redirect('common:collection_cornice_color_list', id=collection_obj.id)
        return render(request, 'common/collection_color_edit.html', context={'form': form})


@login_required(login_url='login')
def CorniceCollectionColorRemove(request, id, color_id):
    collection = CorniceCollection.objects.get(pk=id)
    color = CorniceCollectionColor.objects.get(pk=color_id)
    collection.color.remove(color)
    return redirect('common:collection_cornice_color_list', id=collection.id)


@login_required(login_url='login')
def CorniceCollectionColorList(request, id):
    collection = CorniceCollection.objects.get(pk=id)
    return render(request, 'common/cornice_collection_color_list.html', context={'color': collection})

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