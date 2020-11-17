from django.shortcuts import render, redirect, HttpResponse
from .models import StorageItemTextile, StorageItemCornice, StorageItemTextileReserve
from itertools import chain
from operator import attrgetter
from materials.models import Textile, Cornice, TextileCollection
from .forms import StorageTextileForm
from datetime import datetime

def Storage(request):
    reserve = StorageItemTextileReserve.objects.all()
    qs = StorageItemTextile.objects.all()
    qc = StorageItemCornice.objects.all()
    collection = StorageItemTextile.objects.all()
    result_list = sorted(
        chain(qs, qc),
        key=attrgetter('date_created'), reverse=True)
    return render(request, 'storage/storage.html', context={'orders': result_list, 'reserve': reserve, 'collection': collection})

def Reserve(request):
    reserve = StorageItemTextileReserve.objects.all()

    return render(request, 'storage/reserve.html', context={'orders': reserve})

def TextileReview(request, collection_id, model_id):
    if collection_id != 'all':
        if model_id != 'all':
            m_id = model_id.replace('%20', ' ')
            get_collection = TextileCollection.objects.get(id=collection_id)
            current_c = get_collection.name
            qs = Textile.objects.filter(collection=get_collection, model=m_id)
        else:
            get_collection = TextileCollection.objects.get(id=collection_id)
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
        get_collection = TextileCollection.objects.get(id=collection_id)
        models = Textile.objects.filter(collection=get_collection).order_by().values('model').distinct()
    else:
        models = None

    return render(request, 'storage/add_textile.html', context={'qs': qs,
                                                                'current_c': current_c,
                                                                'current_m': current_m,
                                                                'collection': collection,
                                                                'models': models})


def StorageTextileAdd(request, id):
    if request.method == 'GET':
        prod_name = Textile.objects.get(pk=id)
        form = StorageTextileForm({'item': prod_name, 'price': prod_name.price_opt})
        return render(request, 'storage/add_textile_storage.html', context={'form': form, 'item': prod_name})

    if request.method == 'POST':
        form = StorageTextileForm(request.POST)
        item = request.POST.get("item", None)
        quantity = request.POST.get("quantity", None)
        price = request.POST.get("price", None)
        price_f = request.POST.get("price_f", None)
        item_check = StorageItemTextile.objects.filter(item=item)
        if item_check:
            instance = item_check[0]
            instance.price = round((instance.price * instance.quantity + float(price)*float(quantity))/(instance.quantity + float(quantity)),2)
            instance.quantity += float(quantity)
            instance.price_f = price_f
            instance.date_created = datetime.now()
            instance.save(update_fields=['quantity', 'price', 'price_f', 'date_created'])
            return redirect('storage:storage')
        else:
            if form.is_valid():
                form.save()
                return redirect('storage:storage')
        return render(request, 'storage/add_textile_storage.html', context={'form': form})


def StorageTextileEdit(request, id):
    if request.method == 'GET':
        prod_g = StorageItemTextile.objects.get(pk=id)
        form = StorageTextileForm({'item': prod_g.item, 'price': prod_g.price, 'quantity': prod_g.quantity, 'type_p': prod_g.type_p})
        return render(request, 'storage/edit_textile_storage.html', context={'form': form, 'item': prod_g})

    if request.method == 'POST':
        form = StorageTextileForm(request.POST)
        item = request.POST.get("item", None)
        quantity = request.POST.get("quantity", None)
        price = request.POST.get("price", None)
        if quantity != None and price != None:
            instance = StorageItemTextile.objects.get(pk=id)
            instance.price = price
            instance.quantity = quantity
            instance.date_created = datetime.now()
            instance.save(update_fields=['quantity', 'price', 'date_created'])
            return redirect('storage:storage')
        return render(request, 'storage/edit_textile_storage.html', context={'form': form})

def StorageTextileRemove(request, id):
    prod_name = StorageItemTextile.objects.get(pk=id)
    prod_name.delete()
    return redirect('storage:storage')
