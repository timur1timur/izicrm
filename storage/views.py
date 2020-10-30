from django.shortcuts import render, redirect, HttpResponse
from .models import StorageItemTextile, StorageItemCornice, StorageItemTextileReserve
from itertools import chain
from operator import attrgetter
from materials.models import Textile, Cornice
from .forms import StorageTextileForm
from datetime import datetime

def Storage(request):
    reserve = StorageItemTextileReserve.objects.all()
    qs = StorageItemTextile.objects.all()
    qc = StorageItemCornice.objects.all()
    result_list = sorted(
        chain(qs, qc),
        key=attrgetter('date_created'), reverse=True)
    return render(request, 'storage/storage.html', context={'orders': result_list, 'reserve': reserve})

def Reserve(request):
    reserve = StorageItemTextileReserve.objects.all()

    return render(request, 'storage/reserve.html', context={'orders': reserve})

def TextileReview(request):
    if request.method == 'GET':
        textile = Textile.objects.all()
        return render(request, 'storage/add_textile.html', context={'textile': textile})

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
        item_check = StorageItemTextile.objects.filter(item=item)
        if item_check:
            instance = item_check[0]
            instance.price = round((instance.price * instance.quantity + float(price)*float(quantity))/(instance.quantity + float(quantity)),2)
            instance.quantity += float(quantity)
            instance.date_created = datetime.now()
            instance.save(update_fields=['quantity', 'price', 'date_created'])
            return redirect('storage:storage')
        else:
            if form.is_valid():
                form.save()
                return redirect('storage:storage')
        return render(request, 'storage/add_textile_storage.html', context={'form': form})


def StorageTextileRemove(request, id):
    prod_name = StorageItemTextile.objects.get(pk=id)
    prod_name.delete()
    return redirect('storage:storage')
