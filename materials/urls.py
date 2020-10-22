from django.urls import path
from django.conf.urls import url

from .views import products



urlpatterns = [
    path('products', products, name='posts_week'),
    ]