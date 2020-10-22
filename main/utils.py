from django.shortcuts import render, redirect, HttpResponse
from markup.models import MarkupMaterialCategory, MarkupCustomerCategory, MarkupCommon, MarkupWorkCategory
from orders.models import Customer, Order, Payment, PaymentCategory, Contract

def ObjectRemove(request, id, ModelVar, var_model, redirect_url=None):
    item = ModelVar.objects.get(pk=id)
    item.delete()
    if var_model == 1:
        sp = item.room
    elif var_model == 2:
        sp = item.order
    elif var_model == 3:
        sp = item.specification
    return redirect(f'main:{redirect_url}', id=sp.pk)

def ObjectRemove3(request, id, ModelVar, redirect_url=None):
    item = ModelVar.objects.get(pk=id)
    item.delete()
    return redirect(f'main:{redirect_url}', id=item.pk)


def ObjectRemove2(request, id, ModelVar, var_model, redirect_url=None):
    item = ModelVar.objects.get(pk=id)
    item.delete()
    if var_model == 1:
        sp = item.room
    elif var_model == 2:
        sp = item.order
    elif var_model == 3:
        sp = item.specification
    return redirect(f'main:{redirect_url}', pk=sp.pk)


def ShortName(value):
    st = value
    spl = st.split(' ')
    name = spl[1][0]
    name2 = spl[2][0]
    ret_name = spl[0] + ' ' + name + '.' + name2 + '.'
    return ret_name

def GetMarkupMaterials(order, type_item):
    cus = Customer.objects.get(order=order)
    markup_cus = MarkupCustomerCategory.objects.get(source_t=cus.source_t)
    markup_id = MarkupMaterialCategory.objects.get(source_t=type_item)
    markup_common = MarkupCommon.objects.get(id=1)
    markup_full = markup_cus.markup * markup_id.markup * markup_common.markup
    return round(markup_full, 2)

def GetMarkupWorks(order, type_item):
    cus = Customer.objects.get(order=order)
    markup_cus = MarkupCustomerCategory.objects.get(source_t=cus.source_t)
    markup_id = MarkupWorkCategory.objects.get(source_t=type_item)
    markup_common = MarkupCommon.objects.get(id=1)
    markup_full = markup_cus.markup * markup_id.markup * markup_common.markup
    return round(markup_full, 2)




