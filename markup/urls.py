from django.urls import path
from .views import MarkupList, MarkupCustomerCategoryEdit, MarkupMaterialCategoryEdit, MarkupWorkCategoryEdit, MarkupCommonEdit

app_name = 'markup'


urlpatterns = [
    path('markup/list/', MarkupList, name="markup_list"),
    path('markup/customer/<id>/', MarkupCustomerCategoryEdit, name="markup_customer_edit"),
    path('markup/material/<id>/', MarkupMaterialCategoryEdit, name="markup_material_edit"),
    path('markup/work/<id>/', MarkupWorkCategoryEdit, name="markup_work_edit"),
    path('markup/common/<id>/', MarkupCommonEdit, name="markup_common_edit"),
]