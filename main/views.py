from django.shortcuts import render, redirect, HttpResponse

from orders.forms import SpecificationForm, OrderTextileForm, OrderCorniceForm, OrderWorkSewingForm, \
    OrderWorkAssemblyForm, RoomForm, CustomerForm, ContractForm, PaymentForm, CustomerStartForm, OrderWorkHangingForm, \
    OrderWorkDeliveryForm
from orders.models import Specification, OrderItemTextile1, OrderItemCornice, OrderItemWorkSewing, \
    OrderItemWorkAssembly, Order, Room, Customer, Contract, OfferVersion, Offer, OrderDoc, Payment, \
    OrderItemWorkHanging, OrderItemWorkDelivery, PaymentCategory
from works.models import Work
from materials.models import Textile, Cornice, TextileCollection

from django.contrib.auth.decorators import login_required

from .utils import ObjectRemove, ObjectRemove2, ShortName, ObjectRemove3, GetMarkupMaterials, GetMarkupWorks
import openpyxl
from django.core.files import File
from os.path import join
from django.conf import settings
from django.contrib.auth.models import User


@login_required(login_url='login')
def home(request):
    current_user = request.user
    u = User.objects.get(id=current_user.id)
    group = u.groups.all()[0]
    print(group)
    if u.groups.filter(name='manager').exists():
        return redirect('common:dashboard_manager')
    if u.groups.filter(name='designer').exists():
        return redirect('common:dashboard_designer')
    if u.groups.filter(name='director').exists():
        return redirect('report:orders')
    return redirect('main:orders')

@login_required(login_url='login')
def SpecificationAdd(request, id):
    if request.method == 'GET':
        sp = Room.objects.get(pk=id)
        form = SpecificationForm({'room': sp, 'order': sp.order})
        return render(request, 'main/create_specification.html', context={'form': form})

    if request.method == 'POST':
        bound_form = SpecificationForm(request.POST)
        sp = Room.objects.get(pk=id)
        source = request.POST.get("source", None)

        if source != None:
            instance = Specification.objects.create(order=sp.order, room=sp, version=source)
            return redirect('main:order_view', id=sp.order.pk)
        return render(request, 'main/create_specification.html', context={'form': bound_form})

@login_required(login_url='login')
def SpecificationCopy(request, id):
    start_obj = Specification.objects.get(pk=id)
    obj = Specification.objects.get(pk=id)
    obj_all = Specification.objects.filter(order=obj.order.pk).all()
    obj.pk = None
    obj.version = 'Standart'
    if obj.status == 1:
        obj.status = 0
    obj.save()


    obj_t = OrderItemTextile1.objects.filter(specification=start_obj.pk).all()
    for ob in obj_t:
        ob.pk = None
        ob.specification = obj
        ob.version = obj.version
        ob.save()



    return redirect('main:order_view', id=obj.order.pk)


@login_required(login_url='login')
def SpecificationRemove(request, id):
    item = Specification.objects.get(pk=id)
    item.delete()
    return redirect('main:order_view', id=item.order.pk)


@login_required(login_url='login')
def RoomAdd(request, id):
    if request.method == 'GET':
        sp = Order.objects.get(pk=id)

        form = RoomForm({'order': sp})
        return render(request, 'main/create_room.html', context={'form': form})

    if request.method == 'POST':
        bound_form = RoomForm(request.POST)
        if bound_form.is_valid:
            sp = Order.objects.get(pk=id)
            new_sp = bound_form.save()
            return redirect('main:order_view', id=sp.pk)
        return render(request, 'main/form_sp_add.html', context={'form': bound_form, 'title': 'Добавить помещение'})

@login_required(login_url='login')
def RoomRemove(request, id):
    return ObjectRemove(request, id, Room, 2, 'order_view')

@login_required(login_url='login')
def RoomChangeStatus(request, id):

    sp = Room.objects.get(pk=id)
    curr_state = sp.status
    if curr_state:
        Room.objects.filter(pk=id).update(status=0)
    else:
        Room.objects.filter(pk=id).update(status=1)
    return redirect('main:order_view', id=sp.order.pk)

@login_required(login_url='login')
def RoomReady(request, id):
    item = Room.objects.get(pk=id)
    sp = item.order
    return redirect('main:order_view', id=sp.pk)

@login_required(login_url='login')
def SpecificationChangeStatus(request, id):
    sp = Specification.objects.get(pk=id)
    curr_state = sp.status
    if curr_state:
        Specification.objects.filter(pk=id).update(status=0)
    else:
        Specification.objects.filter(pk=id).update(status=1)
        textile_list = OrderItemTextile1.objects.filter(specification=sp)
        cornice_list = OrderItemCornice.objects.filter(specification=sp)
        sewing_list = OrderItemWorkSewing.objects.filter(specification=sp)
        assembly_list = OrderItemWorkAssembly.objects.filter(specification=sp)
        hanging_list = OrderItemWorkHanging.objects.filter(specification=sp)
        delivery_list = OrderItemWorkDelivery.objects.filter(specification=sp)

        summ_t = 0
        for obj_i in textile_list:
            iter1 = obj_i.total_price()
            summ_t += iter1
        summ_c = 0
        for obj_i in cornice_list:
            iter1 = obj_i.total_price()
            summ_c += iter1

        summ_s = 0
        for obj_i in sewing_list:
            iter1 = obj_i.total_price()
            summ_s += iter1

        summ_a = 0
        for obj_i in assembly_list:
            iter1 = obj_i.total_price()
            summ_a += iter1

        summ_h = 0
        for obj_i in hanging_list:
            iter1 = obj_i.total_price()
            summ_h += iter1

        summ_d = 0
        for obj_i in delivery_list:
            iter1 = obj_i.total_price()
            summ_d += iter1


        total = round((summ_t+summ_c+summ_s+summ_a+summ_h+summ_d), 2)
        sp.textile_total = round(summ_t, 2)
        sp.cornice_total = round(summ_c, 2)
        sp.sewing_total = round(summ_s, 2)
        sp.assembly_total = round(summ_a, 2)
        sp.hanging_total = round(summ_s, 2)
        sp.delivery_total = round(summ_a, 2)
        sp.total = total
        sp.save(update_fields=['textile_total', 'cornice_total', 'sewing_total',
                               'assembly_total', 'hanging_total', 'delivery_total', 'total'])

    return redirect('main:order_view', id=sp.order.pk)

@login_required(login_url='login')
def SpecificationReady(request, id):
    item = Specification.objects.get(pk=id)
    sp = item.room
    return redirect('main:order_view', id=item.order.pk)

@login_required(login_url='login')
def OrderViewD(request, id):
    qs = Order.objects.get(pk=id)
    sp = Room.objects.filter(order=qs)
    check_ready = Room.objects.filter(order=qs, status=True)
    chec_offer = OfferVersion.objects.filter(order=qs)
    check_doc = OrderDoc.objects.filter(order=qs)
    select_offer_q = Offer.objects.filter(order=qs)
    check_prepay = Payment.objects.filter(order=qs)
    customer = Customer.objects.get(order=qs)
    spec = Specification.objects.filter(order=qs)

    if check_ready:
        room_ready = True
    else:
        room_ready = False

    if chec_offer:
        kp_select = True
    else:
        kp_select = False

    if select_offer_q:
        kp_ready = True
    else:
        kp_ready = False

    if check_doc:
        contract_create = True
    else:
        contract_create = False

    if qs.status > 3:
        contract_ready = True
    else:
        contract_ready = False

    if check_prepay:
        prepay_ready = True
    else:
        prepay_ready = False

    state = {
        'room_ready': room_ready,
        'kp_select': kp_select,
        'kp_ready': kp_ready,
        'contract_create': contract_create,
        'contract_ready': contract_ready,
        'prepay_ready': prepay_ready,
        # 'discount': qs.discount,
        # 'discount_s': qs.discount_s

    }

    # if request.method == 'POST':
    #     discount = request.POST.get('discount', None)
    #     print(discount)
    #     if discount != None:
    #         curr_state = qs.discount_s
    #         if curr_state == 0 or curr_state == 3:
    #             qs.discount_s = 1
    #             qs.discount = float(discount)/100
    #             qs.save(update_fields=['discount', 'discount_s'])
    #         return redirect('main:order_view', id=qs.pk)


    context = {
        'qs': qs,
        'sp': sp,
        'doc_qs': check_doc,
        'offers': chec_offer,
        'prepay': check_prepay,
        'customer': customer,
        'spec': spec,
        'state': state
    }
    return render(request, 'main/order_v_.html', context)

@login_required(login_url='login')
def GetDiscount(request, id):
    qs = Order.objects.get(pk=id)

    if request.method == 'GET':
        context = {
            'qs': qs
        }
        return render(request, 'main/add_discount.html', context)


    if request.method == 'POST':
        discount_t = request.POST.get('discount_textile', None)
        discount_c = request.POST.get('discount_cornice', None)
        discount_w = request.POST.get('discount_work', None)
        print(discount_t, discount_c, discount_w)
        if discount_t != None:
            curr_state = qs.discount_t_s
            if curr_state == 0 or curr_state == 3:
                qs.discount_t_s = 1
                qs.discount_t = 1 - float(discount_t)/100
                qs.save(update_fields=['discount_t', 'discount_t_s'])
        if discount_c != None:
            curr_state = qs.discount_c_s
            if curr_state == 0 or curr_state == 3:
                qs.discount_c_s = 1
                qs.discount_c = 1 - float(discount_c)/100
                qs.save(update_fields=['discount_c', 'discount_c_s'])
        if discount_w != None:
            curr_state = qs.discount_w_s
            if curr_state == 0 or curr_state == 3:
                qs.discount_w_s = 1
                qs.discount_w = 1 - float(discount_w)/100
                qs.save(update_fields=['discount_w', 'discount_w_s'])

        if discount_t != None or discount_c != None or discount_w != None:
            curr_state = qs.discount_status
            if curr_state == 0 or curr_state == 3:
                qs.discount_status = 1
                qs.save(update_fields=['discount_status'])

    return redirect('main:order_view', id=qs.pk)

@login_required(login_url='login')
def RefreshDiscount(request, id):
    qs = Order.objects.get(pk=id)
    sp = Specification.objects.filter(order=qs)
    for q in sp:
        textile_list = OrderItemTextile1.objects.filter(specification=q)
        cornice_list = OrderItemCornice.objects.filter(specification=q)
        sewing_list = OrderItemWorkSewing.objects.filter(specification=q)
        assembly_list = OrderItemWorkAssembly.objects.filter(specification=q)
        hanging_list = OrderItemWorkHanging.objects.filter(specification=q)
        delivery_list = OrderItemWorkDelivery.objects.filter(specification=q)

        summ_t = 0
        for obj_i in textile_list:
            iter1 = obj_i.total_price()
            summ_t += iter1
        summ_c = 0
        for obj_i in cornice_list:
            iter1 = obj_i.total_price()
            summ_c += iter1

        summ_s = 0
        for obj_i in sewing_list:
            iter1 = obj_i.total_price()
            summ_s += iter1

        summ_a = 0
        for obj_i in assembly_list:
            iter1 = obj_i.total_price()
            summ_a += iter1

        summ_h = 0
        for obj_i in hanging_list:
            iter1 = obj_i.total_price()
            summ_h += iter1

        summ_d = 0
        for obj_i in delivery_list:
            iter1 = obj_i.total_price()
            summ_d += iter1

        total = round((summ_t + summ_c + summ_s + summ_a + summ_h + summ_d), 2)
        q.textile_total = round(summ_t, 2)
        q.cornice_total = round(summ_c, 2)
        q.sewing_total = round(summ_s, 2)
        q.assembly_total = round(summ_a, 2)
        q.hanging_total = round(summ_s, 2)
        q.delivery_total = round(summ_a, 2)
        q.total = total
        q.save(update_fields=['textile_total', 'cornice_total', 'sewing_total',
                               'assembly_total', 'hanging_total', 'delivery_total', 'total'])
    qs.status = 0
    qs.save(update_fields=['status'])

    offers = OfferVersion.objects.filter(order=qs)
    for offer in offers:
        offer.delete()

    return redirect('main:order_view', id=qs.pk)


@login_required(login_url='login')
def SpecificationViewD(request, pk):
    qs = Specification.objects.get(pk=pk)
    textile_list = OrderItemTextile1.objects.filter(specification=qs)
    cornice_list = OrderItemCornice.objects.filter(specification=qs)
    sewing_list = OrderItemWorkSewing.objects.filter(specification=qs)
    assembly_list = OrderItemWorkAssembly.objects.filter(specification=qs)
    hanging_list = OrderItemWorkHanging.objects.filter(specification=qs)
    delivery_list = OrderItemWorkDelivery.objects.filter(specification=qs)

    summ_t = 0
    for obj_i in textile_list:
        iter1 = obj_i.total_price()
        summ_t += iter1

    summ_c = 0
    for obj_i in cornice_list:
        iter1 = obj_i.total_price()
        summ_c += iter1

    summ_s = 0
    for obj_i in sewing_list:
        iter1 = obj_i.total_price()
        summ_s += iter1

    summ_a = 0
    for obj_i in assembly_list:
        iter1 = obj_i.total_price()
        summ_a += iter1

    summ_h = 0
    for obj_i in hanging_list:
        iter1 = obj_i.total_price()
        summ_h += iter1

    summ_d = 0
    for obj_i in delivery_list:
        iter1 = obj_i.total_price()
        summ_d += iter1


    context = {
        'qs': qs,
        'textile': textile_list,
        'cornice': cornice_list,
        'sewing': sewing_list,
        'assembly': assembly_list,
        'hanging': hanging_list,
        'delivery': delivery_list,
        'summ_t': round(summ_t, 2),
        'summ_c': round(summ_c, 2),
        'summ_s': round(summ_s, 2),
        'summ_a': round(summ_a, 2),
        'summ_h': round(summ_h, 2),
        'summ_d': round(summ_d, 2),
        'summ': round((summ_t+summ_c+summ_s+summ_a+summ_h+summ_d), 2),
    }

    return render(request, 'main/specification_v_.html', context)

from storage.models import StorageItemTextile, StorageItemTextileReserve

@login_required(login_url='login')
def TextileReview(request, id, collection_id, model_id):

    sp = Specification.objects.get(pk=id)
    textile_storage = StorageItemTextile.objects.all()

    if collection_id != 'all':
        if model_id != 'all':
            get_collection = TextileCollection.objects.get(name__iexact=collection_id)
            current_c = get_collection.name
            qs = Textile.objects.filter(collection=get_collection, model=model_id)
        else:
            get_collection = TextileCollection.objects.get(name__iexact=collection_id)
            current_c = get_collection.name
            qs = Textile.objects.filter(collection=get_collection)
    else:
        qs = Textile.objects.all()[:100]
        current_c = 'all'

    current_m = model_id
    collection = TextileCollection.objects.all()
    if collection_id != 'all':
        get_collection = TextileCollection.objects.get(name__iexact=collection_id)
        models = Textile.objects.filter(collection=get_collection).order_by().values('model').distinct()
    else:
        models = None

    markup = GetMarkupMaterials(sp.order, 0)
    return render(request, 'main/add_textile.html', context={'qs': qs,
                                                             'storage': textile_storage,
                                                             'id': id,
                                                             'markup': markup,
                                                             'current_c': current_c,
                                                             'current_m': current_m,
                                                             'collection': collection,
                                                             'models': models
                                                             })


from django.db.models import Sum
from datetime import datetime

@login_required(login_url='login')
def SpecificationTextileAdd(request, id, prod_id):
    if request.method == 'GET':
        sp = Specification.objects.get(pk=id)
        markup = GetMarkupMaterials(sp.order, 0)
        prod_name = Textile.objects.get(pk=prod_id)
        textile_storage = StorageItemTextile.objects.filter(item=prod_id)
        if textile_storage:
            t_s = textile_storage[0]
        else:
            t_s = 0
        form = OrderTextileForm({'specification': sp, 'order': sp.order, 'item': prod_id, 'markup': markup})
        return render(request, 'main/add_textile_order.html', context={'form': form, 'prod_name': prod_name, 'storage': t_s})

    if request.method == 'POST':
        sp = Specification.objects.get(pk=id)
        form = OrderTextileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:spec', pk=sp.pk)

@login_required(login_url='login')
def SpecificationTextileEdit(request, id):
    if request.method == 'GET':

        prod_name = OrderItemTextile1.objects.get(pk=id)
        form = OrderTextileForm({'quantity': prod_name.quantity})
        return render(request, 'main/edit_textile_order.html', context={'form': form, 'prod_name': prod_name.item})

    if request.method == 'POST':
        prod_name = OrderItemTextile1.objects.get(pk=id)
        form = OrderTextileForm(request.POST)
        quantity = request.POST.get("quantity", None)

        if quantity != None:
            instance = OrderItemTextile1.objects.get(pk=id)
            instance.quantity = quantity
            instance.save(update_fields=['quantity'])
            return redirect('main:spec', pk=prod_name.specification.pk)
        return render(request, 'main/edit_textile_order.html', context={'form': form, 'prod_name': prod_name.item})


@login_required(login_url='login')
def SpecificationTextileRemove(request, id):
    return ObjectRemove2(request, id, OrderItemTextile1, 3, 'spec')

@login_required(login_url='login')
def CorniceReview(request, id):
    if request.method == 'GET':
        sp = Specification.objects.get(pk=id)
        cornice = Cornice.objects.all()
        markup = GetMarkupMaterials(sp.order, 1)
        return render(request, 'main/add_cornice.html', context={'cornice': cornice, 'id': id, 'markup': markup})

@login_required(login_url='login')
def SpecificationCorniceAdd(request, id, prod_id):
    if request.method == 'GET':
        sp = Specification.objects.get(pk=id)
        prod_name = Cornice.objects.get(pk=prod_id)
        markup = GetMarkupMaterials(sp.order, 1)
        form = OrderCorniceForm({'specification': sp, 'order': sp.order, 'item': prod_id, 'markup': markup})
        return render(request, 'main/add_cornice_order.html', context={'form': form, 'prod_name': prod_name})

    if request.method == 'POST':
        sp = Specification.objects.get(pk=id)
        form = OrderCorniceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:spec', pk=sp.pk)

@login_required(login_url='login')
def SpecificationCorniceRemove(request, id):
    return ObjectRemove2(request, id, OrderItemCornice, 3, 'spec')

@login_required(login_url='login')
def SpecificationSewingAdd(request, id):
    if request.method == 'GET':
        sp = Specification.objects.get(pk=id)
        markup = GetMarkupWorks(sp.order, 0)
        form = OrderWorkSewingForm({'specification': sp, 'order': sp.order, 'markup': markup})
        return render(request, 'main/add_sewing_order.html', context={'form': form})

    if request.method == 'POST':
        sp = Specification.objects.get(pk=id)
        form = OrderWorkSewingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:spec', pk=sp.pk)

@login_required(login_url='login')
def SpecificationSewingRemove(request, id):
    return ObjectRemove2(request, id, OrderItemWorkSewing, 3, 'spec')

@login_required(login_url='login')
def SpecificationAssemblyAdd(request, id):
    if request.method == 'GET':
        sp = Specification.objects.get(pk=id)
        markup = GetMarkupWorks(sp.order, 1)
        form = OrderWorkAssemblyForm({'specification': sp, 'order': sp.order, 'markup': markup})
        return render(request, 'main/add_assembly_order.html', context={'form': form, 'title': 'монтаж'})

    if request.method == 'POST':
        sp = Specification.objects.get(pk=id)
        form = OrderWorkAssemblyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:spec', pk=sp.pk)

@login_required(login_url='login')
def SpecificationAssemblyRemove(request, id):
    return ObjectRemove2(request, id, OrderItemWorkAssembly, 3, 'spec')

@login_required(login_url='login')
def SpecificationHangingAdd(request, id):
    if request.method == 'GET':
        sp = Specification.objects.get(pk=id)
        markup = GetMarkupWorks(sp.order, 2)
        form = OrderWorkHangingForm({'specification': sp, 'order': sp.order, 'markup': markup})
        return render(request, 'main/add_assembly_order.html', context={'form': form, 'title': 'развеску штор'})

    if request.method == 'POST':
        sp = Specification.objects.get(pk=id)
        form = OrderWorkHangingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:spec', pk=sp.pk)

@login_required(login_url='login')
def SpecificationHangingRemove(request, id):
    return ObjectRemove2(request, id, OrderItemWorkHanging, 3, 'spec')

@login_required(login_url='login')
def SpecificationDeliveryAdd(request, id):
    if request.method == 'GET':
        sp = Specification.objects.get(pk=id)
        markup = GetMarkupWorks(sp.order, 3)
        form = OrderWorkDeliveryForm({'specification': sp, 'order': sp.order, 'markup': markup})
        return render(request, 'main/add_assembly_order.html', context={'form': form, 'title': 'доставку'})

    if request.method == 'POST':
        sp = Specification.objects.get(pk=id)
        form = OrderWorkDeliveryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:spec', pk=sp.pk)

@login_required(login_url='login')
def SpecificationDeliveryRemove(request, id):
    return ObjectRemove2(request, id, OrderItemWorkDelivery, 3, 'spec')


@login_required(login_url='login')
def OrderView(request):
    qs = Order.objects.all().order_by('-date_created')
    rooms = Room.objects.all()
    customer = Customer.objects.all()
    context = {
        'orders': qs,
        'room': rooms,
        'customer': customer
    }
    return render(request, 'main/orders_.html', context)

@login_required(login_url='login')
def OrderCreate(request):
    if request.method == 'GET':

        form = CustomerStartForm()
        if Customer.objects.all():
            customers = Customer.objects.all()
        else:
            customers = None
        return render(request, 'main/create_order.html', context={'form': form, 'customers': customers})

    if request.method == 'POST':

        form = CustomerStartForm(request.POST)
        source = request.POST.get("source", None)
        customer = request.POST.get("name", None)
        email = request.POST.get("email", None)
        phone = request.POST.get("phone", None)

        if source != None and customer != None:
            item = Order.objects.create(user=request.user)

            instance = Customer.objects.create(name=customer, email=email, phone=phone, source_t=source)
            instance.order.add(item.pk)
            return redirect('main:order_view', id=item.pk)
        return render(request, 'main/create_order.html', context={'form': form})

@login_required(login_url='login')
def OrderCreateCustomer(request, id):
    cust = Customer.objects.get(pk=id)
    if cust:
        item = Order.objects.create(user=request.user)
        cust.order.add(item.pk)
    return redirect('main:order_view', id=item.pk)

@login_required(login_url='login')
def OrderRemove(request, id):
    item = Order.objects.get(pk=id)
    item.delete()
    return redirect('main:orders')

@login_required(login_url='login')
def OrderArchive(request, id):
    item = Order.objects.get(pk=id)

    item.status = 11
    item.status_css = 11
    item.progress = 11
    item.save(update_fields=['status', 'progress', 'status_css'])

    return redirect('main:orders')

@login_required(login_url='login')
def Test(request):
    qs = Order.objects.all()
    context = {
        'orders': qs
    }
    return render(request, 'main/pages-invoice.html', context)


@login_required(login_url='login')
def OrderCreateKp(request, id):
    qs = Order.objects.get(pk=id)
    rooms = Room.objects.filter(order=qs, status=True)
    mass_rooms = {}
    for room in rooms:
        mass_sp = {}
        mass_rooms[room.name] = mass_sp
        spd = Specification.objects.filter(room=room, status=True)
        for sp in spd:
            if qs.discount_t < 1 or qs.discount_c < 1 or qs.discount_w < 1:
                mass_var = {}
                mass_var['textile'] = sp.textile_total
                mass_var['textile_d'] = round(float(sp.textile_total) - float(sp.textile_total)/qs.discount_t, 2)
                mass_var['cornice'] = sp.cornice_total
                mass_var['cornice_d'] = round(float(sp.cornice_total) - float(sp.cornice_total)/qs.discount_c, 2)
                mass_var['sewing'] = sp.sewing_total
                mass_var['sewing_d'] = round(float(sp.sewing_total) - float(sp.sewing_total)/qs.discount_w, 2)
                mass_var['assembly'] = sp.assembly_total
                mass_var['assembly_d'] = round(float(sp.assembly_total) - float(sp.assembly_total)/qs.discount_w, 2)
                mass_var['hanging'] = sp.hanging_total
                mass_var['hanging_d'] = round(float(sp.hanging_total) - float(sp.hanging_total)/qs.discount_w, 2)
                mass_var['delivery'] = sp.delivery_total
                mass_var['delivery_d'] = round(float(sp.delivery_total) - float(sp.delivery_total)/qs.discount_w, 2)

                temp_var = round(float(sp.textile_total) - float(sp.textile_total)/qs.discount_t, 2) \
                           + round(float(sp.cornice_total) - float(sp.cornice_total)/qs.discount_c, 2) \
                           + round(float(sp.sewing_total) - float(sp.sewing_total)/qs.discount_w, 2) \
                           + round(float(sp.assembly_total) - float(sp.assembly_total)/qs.discount_w, 2) \
                           + round(float(sp.hanging_total) - float(sp.hanging_total)/qs.discount_w, 2) \
                           + round(float(sp.delivery_total) - float(sp.delivery_total)/qs.discount_w, 2)
                mass_var['total'] = sp.total
                mass_var['total_d'] = round(temp_var, 2)
                mass_sp[sp.version] = mass_var
            else:
                mass_var = {}
                mass_var['textile'] = sp.textile_total
                mass_var['cornice'] = sp.cornice_total
                mass_var['sewing'] = sp.sewing_total
                mass_var['assembly'] = sp.assembly_total
                mass_var['hanging'] = sp.hanging_total
                mass_var['delivery'] = sp.delivery_total
                mass_var['total'] = sp.total
                mass_sp[sp.version] = mass_var

    if qs.discount_t < 1 or qs.discount_c < 1 or qs.discount_w < 1:
        dis_state = {
            'textile': round((1 - qs.discount_t)*100, 2),
            'cornice': round((1 - qs.discount_c)*100, 2),
            'work': round((1 - qs.discount_w)*100, 2)
        }
    else:
        dis_state = {}


    econom_v = 0
    standart_v = 0
    premium_v = 0

    for q in mass_rooms:
        for sp in mass_rooms[q]:
            if sp == 'Econom':
                econom_v += float(mass_rooms[q][sp]['total'])
            if sp == 'Standart':
                standart_v += float(mass_rooms[q][sp]['total'])
            if sp == 'Premium':
                premium_v += float(mass_rooms[q][sp]['total'])

    finish_mass = {
        'econom': round(econom_v, 2),
        'standart': round(standart_v, 2),
        'premium': round(premium_v, 2)
    }

    context = {
        'order': qs,
        'rooms': rooms,
        'sps': mass_rooms,
        'dis_state': dis_state,
        'finish': finish_mass
    }

    return render(request, 'main/pages-invoice.html', context)


@login_required(login_url='login')
def CustomerCreate(request, id):
    if request.method == 'GET':
        sp = Order.objects.get(pk=id)
        customer = Customer.objects.get(order=sp)

        form = CustomerForm({
            'order': sp,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'address': customer.address,
            'pass_series': customer.pass_series,
            'pass_number': customer.pass_number,
            'pass_date': customer.pass_date,
            'pass_issued': customer.pass_issued,
            'source_t': customer.source_t

        })
        return render(request, 'main/create_customer2.html', context={'form': form})

    if request.method == 'POST':
        bound_form = CustomerForm(request.POST)
        
        name = request.POST.get("name", None)
        phone = request.POST.get("phone", None)
        email = request.POST.get("email", None)
        address = request.POST.get("address", None)
        pass_series = request.POST.get("pass_series", None)
        pass_number = request.POST.get("pass_number", None)
        pass_date = request.POST.get("pass_date", None)
        pass_issued = request.POST.get("pass_issued", None)
        source_t = request.POST.get("source_t", None)


        if bound_form.is_valid:
            sp = Order.objects.get(pk=id)
            instance = Customer.objects.get(order=sp)
            instance.name = name
            instance.phone = phone
            instance.email = email
            instance.address = address
            instance.pass_series = pass_series
            instance.pass_number = pass_number
            instance.pass_date = pass_date
            instance.pass_issued = pass_issued
            instance.source_t = source_t

            instance.save()
            return redirect('main:contract_create', id=sp.pk)
        return render(request, 'main/create_customer2.html', context={'form': bound_form})

@login_required(login_url='login')
def ContractCreate(request, id):
    if request.method == 'GET':
        sp = Order.objects.get(pk=id)
        cus = Customer.objects.filter(order=sp)[0]
        offr = Offer.objects.filter(order=sp)[0]
        form = ContractForm({'order': sp, 'customer': cus, 'price': float(offr.version.total)})
        return render(request, 'main/create_contract.html', context={'form': form, 'order': sp.number, 'customer': cus.name})

    if request.method == 'POST':
        bound_form = ContractForm(request.POST)
        if bound_form.is_valid:
            sp = Order.objects.get(pk=id)
            new_sp = bound_form.save()
            return redirect('main:contract_create_xls', id=sp.pk)
        return render(request, 'main/create_contract.html', context={'form': bound_form, 'title': 'Добавить договор'})

@login_required(login_url='login')
def ContractCreateXls(request, id):
    order_id = Order.objects.get(pk=id)
    customer_qs = Customer.objects.filter(order=order_id)[0]

    wb = openpyxl.load_workbook(filename='contract_test.xlsx')
    sheet = wb['Договор']

    # Номер договора
    sheet_order_name = 'A2'
    # Дата договора
    sheet_order_date_created = 'F4'

    # ФИО заказчика
    sheet_customer_name = 'A6'
    # ФИО заказчика
    sheet_customer_name2 = 'A80'
    # Телефон заказчика
    sheet_customer_phone = 'A84'
    # Адрес заказчика
    sheet_customer_address = 'A82'
    # Серия заказчика
    sheet_customer_pass_series = 'A86'
    # Номер заказчика
    sheet_customer_pass_number = 'A87'
    # Дата выдачи заказчика
    sheet_customer_pass_date = 'A88'
    # Выдан заказчика
    sheet_customer_pass_issued = 'A89'
    # Подпись/ФИО заказчика
    sheet_customer_short_name = 'A100'

    sheet[sheet_order_name] = sheet[sheet_order_name].value + ' ' + order_id.number
    sheet[sheet_order_date_created] = order_id.date_created

    sheet[sheet_customer_name] = customer_qs.name + sheet[sheet_customer_name].value
    sheet[sheet_customer_name2] = customer_qs.name
    sheet[sheet_customer_phone] = customer_qs.phone
    sheet[sheet_customer_address] = customer_qs.address
    sheet[sheet_customer_pass_series] = sheet[sheet_customer_pass_series].value + ' ' + customer_qs.pass_series
    sheet[sheet_customer_pass_number] = sheet[sheet_customer_pass_number].value + ' ' + customer_qs.pass_number
    sheet[sheet_customer_pass_date] = sheet[sheet_customer_pass_date].value + ' ' + customer_qs.pass_date
    sheet[sheet_customer_pass_issued] = sheet[sheet_customer_pass_issued].value + ' ' + customer_qs.pass_issued
    sheet[sheet_customer_short_name] = sheet[sheet_customer_short_name].value + ' ' + ShortName(customer_qs.name) + ' /'

    wb.save(f'contract_{order_id.number}.xlsx')

    context = {
        'test': 'Договор сохранен'
    }
    return render(request, 'main/contract.html', context)

@login_required(login_url='login')
def OfferCreate(request, id):
    sp = Order.objects.get(pk=id)
    rooms = Room.objects.filter(order=sp, status=True)
    total_econom = 0
    total_standart = 0
    total_premium = 0
    mass_rooms = {}
    for room in rooms:
        mass_sp = {}
        mass_rooms[room.name] = mass_sp
        spd = Specification.objects.filter(room=room, status=True)
        for sp1 in spd:
            mass_sp[sp1.version] = sp1.total

    for key in mass_rooms:
        fp = mass_rooms[key]
        for key in fp:
            gg = fp[key]
            if key == 'Econom':
                total_econom += float(gg)
            elif key == 'Standart':
                total_standart += float(gg)
            elif key == 'Premium':
                total_premium += float(gg)

    if total_econom > 0:
        offer = OfferVersion.objects.create(order=sp, version='Econom', total=round(total_econom,2))
    if total_standart > 0:
        offer = OfferVersion.objects.create(order=sp, version='Standart', total=round(total_standart,2))
    if total_premium > 0:
        offer = OfferVersion.objects.create(order=sp, version='Premium', total=round(total_premium,2))

    curr_state = sp.status

    if curr_state == 0:
        sp.status = 1
        sp.status_css = 1
        sp.progress = 1
        sp.save(update_fields=['status', 'progress', 'status_css'])

    return redirect('main:order_view', id=sp.pk)

@login_required(login_url='login')
def OfferSelect(request, id):
    sp = OfferVersion.objects.get(pk=id)
    Offer.objects.create(order=sp.order, version=sp)
    curr_state = sp.order.status
    if curr_state == 1:
        sp.order.status = 2
        sp.order.status_css = 2
        sp.progress = 2
        sp.order.save(update_fields=['status', 'progress', 'status_css'])
    return redirect('main:order_view', id=sp.order.pk)


from docxtpl import DocxTemplate

@login_required(login_url='login')
def ContractCreateWord(request, id):

    order_id = Order.objects.get(pk=id)
    customer_id = Customer.objects.filter(order=order_id)[0]
    contract_id = Contract.objects.filter(order=order_id)[0]

    path = join(settings.MEDIA_ROOT, f'conract_{order_id.number}.docx')
    f = open(path, "w+b")

    doc = DocxTemplate("contract_template.docx")
    context = {
        'contract_number': order_id.number,
        'contract_date': order_id.date_created.strftime('%d.%m.%Y'),
        'contract_garant': contract_id.garant,
        'contract_price': contract_id.price,
        'contract_price2': contract_id.price_w,
        'contract_prepay': contract_id.prepay,
        'contract_prepay_duration': contract_id.prepay_duration,
        'contract_work_start': contract_id.work_start,
        'contract_work_duration': contract_id.work_duration,
        'customer_name': customer_id.name,
        'customer_phone': customer_id.phone,
        'customer_address': customer_id.address,
        'cus_pass_series': customer_id.pass_series,
        'cus_pass_number': customer_id.pass_number,
        'cus_pass_date': customer_id.pass_date,
        'cus_pass_issued': customer_id.pass_issued,
        # 'customer_name_short': ShortName(customer_id.name)
    }

    doc.render(context)
    doc.save(f)

    contract_file = OrderDoc()
    contract_file.order = order_id
    contract_file.contract_doc.name = path
    contract_file.save()

    curr_state = order_id.status
    if curr_state == 2:
        order_id.status = 3
        order_id.status_css = 3
        order_id.progress = 3
        order_id.save(update_fields=['status', 'progress', 'status_css'])

    return redirect('main:order_view', id=order_id.pk)


@login_required(login_url='login')
def GetContract(request, id):
    order_id = Order.objects.get(pk=id)
    contract_date = order_id.date_created.strftime('%Y%m%d')
    doc_contract = OrderDoc.objects.get(order=order_id)
    response = HttpResponse(doc_contract.contract_doc, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={contract_date}_contract_{order_id.number}.docx'
    return response


@login_required(login_url='login')
def ContractReady(request, id):
    sp = Order.objects.get(pk=id)
    curr_state = sp.status
    if curr_state == 3:
        sp.status = 4
        sp.status_css = 4
        sp.progress = 4
        sp.save(update_fields=['status', 'progress', 'status_css'])

    offer = Offer.objects.get(order=sp)
    textile = OrderItemTextile1.objects.filter(order=sp, version=offer.version.version)
    for t in textile:
        item_storage = StorageItemTextile.objects.filter(item=t.item)
        print(item_storage)
        if item_storage:
            item_storage_q = item_storage[0].quantity
            item_reserve_q = StorageItemTextileReserve.objects.filter(item=item_storage[0]).aggregate(Sum('quantity'))['quantity__sum']
            if item_storage_q > 0 and item_reserve_q != None:
                check_q = item_storage_q - item_reserve_q - t.quantity
            elif item_storage_q > 0 and item_reserve_q == None:
                check_q = item_storage_q - t.quantity
        if check_q > 0 or check_q == 0:
            instance = StorageItemTextileReserve.objects.create(
                    order=sp,
                    item=item_storage[0],
                    quantity=t.quantity
                )


        # if storage != None and storage != 0:
        #     item_storage = StorageItemTextile.objects.filter(item=item)[0]
        #     instance = StorageItemTextileReserve.objects.create(
        #         order=sp.order,
        #         item=item_storage,
        #         quantity=quantity
        #     )
    return redirect('main:order_view', id=sp.pk)

@login_required(login_url='login')
def PaymentCreate(request, id):
    order_id = Order.objects.get(pk=id)
    payments_qs = Payment.objects.filter(order=order_id)
    if payments_qs.exists():
        if request.method == 'GET':
            sp = Order.objects.get(pk=id)
            cus = Customer.objects.filter(order=sp)[0]
            user = request.user
            category = PaymentCategory.objects.get(name='Платеж')
            form = PaymentForm({'order': sp, 'customer': cus, 'category': category, 'user': user})
            return render(request, 'main/create_payment.html', context={'form': form, 'title': 'платежа', 'order': sp.number, 'category': category.name})
    else:
        if request.method == 'GET':
            sp = Order.objects.get(pk=id)
            cus = Customer.objects.filter(order=sp)[0]
            user = request.user
            category = PaymentCategory.objects.get(name='Аванс')
            form = PaymentForm({'order': sp, 'customer': cus, 'category': category, 'user': user})
            return render(request, 'main/create_payment.html', context={'form': form, 'title': 'первичного аванса', 'order': sp.number,'category': category.name})

    if request.method == 'POST':
        bound_form = PaymentForm(request.POST)
        sp = Order.objects.get(pk=id)
        category = request.POST.get("category", None)
        type_money = request.POST.get("type_money", None)
        price = request.POST.get("price", None)
        receipt = request.POST.get("receipt", None)
        if category != None and type_money != None and price != None and receipt != None:
            cat = PaymentCategory.objects.get(pk=category)
            instance = Payment.objects.create(
                order=sp,
                category=cat,
                type_money=type_money,
                price=price,
                receipt=receipt,
                user=request.user
            )
            curr_state = sp.status
            if curr_state == 4:
                sp.status = 5
                sp.status_css = 5
                sp.progress = 5
                sp.save(update_fields=['status', 'progress', 'status_css'])
            return redirect('main:order_view', id=sp.pk)

        return render(request, 'main/form_sp_add.html', context={'form': bound_form, 'title': 'Добавить договор'})

@login_required(login_url='login')
def TestTemplate(request):
    qs = Order.objects.all()
    context = {
        'orders': qs
    }
    return render(request, 'main/orders_.html', context)

