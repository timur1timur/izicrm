from django.shortcuts import render
from django.http import HttpResponse
from .models import Textile, Cornice


def products(request):
    textile = Textile.objects.all()
    cornice = Cornice.objects.all()
    context = {
        'textile': textile,
        'cornice': cornice
    }

    return render(request, 'materials/products.html', context)


