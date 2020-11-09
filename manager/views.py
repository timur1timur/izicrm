from django.shortcuts import render, redirect
from orders.models import Order, Offer, Room, Specification, OrderItemTextile1, OrderItemCornice, OrderItemWorkSewing, \
    OrderItemWorkAssembly, SupplierOrder, SupplierOrderCornice, Customer, Contract, OrderItemWorkHanging, \
    OrderItemWorkDelivery, Payment, PaymentCategory, TrackedOrder, OrderItemCorniceAdditional
from .forms import SupplierOrderedTextileForm, PaymentFormManager, SupplierForm, SupplierOrderedCorniceForm
from .models import SupplierOrderedTextile, SupplierOrderedCornice
from .utils import SendTo, mailanalytics, M_StatusMaterialsCheck, M_ChangeOrderState, M_GetStatusMaterialOrder, \
    M_ChangeWorkOrderState, CheckDiscountState
from django.contrib.auth.decorators import login_required



@login_required(login_url='login')
def M_OrderView(request):
    qs = Order.objects.filter(status__gte=5, status__lte=10).order_by('-date_created')
    customer = Customer.objects.all()
    context = {
        'orders': qs,
        'customer': customer
    }
    return render(request, 'manager/orders_.html', context)


from storage.models import StorageItemTextile, StorageItemTextileReserve


@login_required(login_url='login')
def M_OrderViewD(request, id):
    qs = Order.objects.get(pk=id)
    offer = Offer.objects.filter(order=qs)[0]
    offer_version = offer.version.get_version_display()
    textile = OrderItemTextile1.objects.filter(order=qs, version=offer_version)
    cornice = OrderItemCornice.objects.filter(order=qs, version=offer_version)
    additional = OrderItemCorniceAdditional.objects.filter(order=qs, version=offer_version)
    sewing = OrderItemWorkSewing.objects.filter(order=qs, version=offer_version)
    assembly = OrderItemWorkAssembly.objects.filter(order=qs, version=offer_version)
    hanging = OrderItemWorkHanging.objects.filter(order=qs, version=offer_version)
    delivery = OrderItemWorkDelivery.objects.filter(order=qs, version=offer_version)
    supplier_order = SupplierOrder.objects.filter(order=qs)
    supplier_order_cornice = SupplierOrderCornice.objects.filter(order=qs)
    customer = Customer.objects.all()
    contract = Contract.objects.get(order=qs)
    reserve = StorageItemTextileReserve.objects.filter(order=qs)
    tracked_order, created = TrackedOrder.objects.get_or_create(order=qs, user=request.user)
    if created:
        qs.user_view = 1
        qs.save()
    print(request.user.id)

    work_quantity = \
        sewing.count() + \
        assembly.count() + \
        hanging.count() + \
        delivery.count()

    work_ordered = \
        sewing.filter(ordered__gte=1).count() + \
        assembly.filter(ordered__gte=1).count() + \
        hanging.filter(ordered__gte=1).count() + \
        delivery.filter(ordered__gte=1).count()

    textile_state = {
        'ordered': textile.filter(ordered__gte=2).count(),
        'payed': textile.filter(ordered__gte=3).count(),
        'shipped': textile.filter(ordered__gte=4).count(),
    }

    cornice_state = {
        'ordered': cornice.filter(ordered__gte=2).count(),
        'payed': cornice.filter(ordered__gte=3).count(),
        'shipped': cornice.filter(ordered__gte=4).count(),
    }

    work_state = {
        'ordered': work_ordered,
        'quantity': work_quantity
    }

    state = {
        'textile': textile_state,
        'cornice': cornice_state,
        'work': work_state
    }

    context = {
        'qs': qs,
        'textile': textile,
        'cornice': cornice,
        'additional': additional,
        'sewing': sewing,
        'assembly': assembly,
        'hanging': hanging,
        'delivery': delivery,
        'supplier_order': supplier_order,
        'supplier_order_cornice': supplier_order_cornice,
        'customer': customer,
        'contract': contract,
        'state': state,
        'reserve': reserve
    }
    return render(request, 'manager/order_v_.html', context)

@login_required(login_url='login')
def M_OrderViewD_Budget(request, id):
    qs = Order.objects.get(pk=id)
    payments_arrival = Payment.objects.filter(order=qs, category__type_p=0)
    payments_expense = Payment.objects.filter(order=qs, category__type_p=1)
    offer = Offer.objects.filter(order=qs)[0]
    offer_version = offer.version.get_version_display()
    textile = OrderItemTextile1.objects.filter(order=qs, version=offer_version)
    cornice = OrderItemCornice.objects.filter(order=qs, version=offer_version)
    sewing = OrderItemWorkSewing.objects.filter(order=qs, version=offer_version)
    assembly = OrderItemWorkAssembly.objects.filter(order=qs, version=offer_version)
    hanging = OrderItemWorkHanging.objects.filter(order=qs, version=offer_version)
    delivery = OrderItemWorkDelivery.objects.filter(order=qs, version=offer_version)

    customer = Customer.objects.all()
    contract = Contract.objects.get(order=qs)

    textile_arrival = 0
    textile_expense = 0
    for t in textile:
        textile_arrival += t.total_price()
        textile_expense += t.item.price_opt * t.quantity

    cornice_arrival = 0
    cornice_expense = 0
    for t in cornice:
        cornice_arrival += t.total_price()
        cornice_expense += t.item.price_opt * t.quantity

    sewing_arrival = 0
    sewing_expense = 0
    for t in sewing:
        sewing_arrival += t.total_price()
        sewing_expense += t.item.price * t.quantity

    assembly_arrival = 0
    assembly_expense = 0
    for t in assembly:
        assembly_arrival += t.total_price()
        assembly_expense += t.item.price * t.quantity

    hanging_arrival = 0
    hanging_expense = 0
    for t in hanging:
        hanging_arrival += t.total_price()
        hanging_expense += t.item.price * t.quantity

    delivery_arrival = 0
    delivery_expense = 0
    for t in delivery:
        delivery_arrival += t.total_price()
        delivery_expense += t.item.price * t.quantity

    total_arrival = textile_arrival + cornice_arrival + sewing_arrival + assembly_arrival + hanging_arrival + delivery_arrival
    total_expense = textile_expense + cornice_expense + sewing_expense + assembly_expense + hanging_expense + delivery_expense
    total_profit = total_arrival - total_expense
    total_change = total_profit*100/total_arrival

    budget_plane = {
        'textile': {
            'arrival': textile_arrival,
            'expense': textile_expense
        },
        'cornice': {
            'arrival': cornice_arrival,
            'expense': cornice_expense
        },
        'sewing': {
            'arrival': sewing_arrival,
            'expense': sewing_expense
        },
        'assembly': {
            'arrival': assembly_arrival,
            'expense': assembly_expense
        },
        'hanging': {
            'arrival': hanging_arrival,
            'expense': hanging_expense
        },
        'delivery': {
            'arrival': delivery_arrival,
            'expense': delivery_expense
        },
        'total': {
            'arrival': round(total_arrival, 2),
            'expense': round(total_expense, 2),
            'profit': round(total_profit, 2),
            'change': round(total_change, 2)
        }
    }

    pay_arrival = 0
    for t in payments_arrival:
        pay_arrival += float(t.price)
    pay_expense = 0
    for t in payments_expense:
        pay_expense += float(t.price)

    pay_profit = pay_arrival - pay_expense


    if pay_expense == 0:
        pay_change = 0
    else:
        pay_change = pay_profit*100/pay_arrival


    budget_fact = {
        'total': {
            'arrival': round(pay_arrival, 2),
            'expense': round(pay_expense, 2),
            'profit': round(pay_profit, 2),
            'change': round(pay_change, 2)
        }
    }
    supp_textile_price = SupplierOrderedTextile.objects.filter(order=id)
    supp_cornice_price = SupplierOrderedCornice.objects.filter(order=id)

    context = {
        'qs': qs,
        'textile': textile,
        'cornice': cornice,
        'sewing': sewing,
        'assembly': assembly,
        'hanging': hanging,
        'delivery': delivery,
        'customer': customer,
        'contract': contract,
        'payments_arrival': payments_arrival,
        'budget_plane': budget_plane,
        'budget_fact': budget_fact,
        'supp_textile': supp_textile_price,
        'supp_cornice': supp_cornice_price
    }
    return render(request, 'manager/order_v_budget.html', context)

@login_required(login_url='login')
def SupplierOrderView(request, id):
    item = OrderItemTextile1.objects.get(pk=id)
    order = item.order
    supplier = item.item.manufacturer

    SuppOrder = SupplierOrder.objects.filter(order=order, supplier=supplier).count()

    if SuppOrder > 0:
        check_SuppOrder = SupplierOrder.objects.get(order=order, supplier=supplier)
        check_SuppOrder.materials.add(item)
    else:
        instance = SupplierOrder.objects.create(order=order, supplier=supplier)
        instance.materials.add(item)

    # render(request, 'manager/index.html', context={})
    return redirect('manager:order_view', id=order.pk)

@login_required(login_url='login')
def SupplierOrderSend(request, id):
    order = SupplierOrder.objects.get(pk=id)
    materials = order.materials.all()
    materials_mass = []
    for m in materials:
        materials_mass.append(m.item.article)
    supplier_email = order.supplier.email
    SendTo(materials_mass, supplier_email, order.order.number)
    curr_state = order.status
    if curr_state == 0:
        order.status = 1
        order.save(update_fields=['status'])
    for mat in materials:
        mat_curr_state = mat.ordered
        if mat_curr_state == 0:
            mat.ordered = 1
            mat.ordered_icon = 1
            mat.save(update_fields=['ordered', 'ordered_icon'])
    return redirect('manager:order_view', id=order.order.pk)

@login_required(login_url='login')
def SupplierOrderCorniceSend(request, id):
    order = SupplierOrderCornice.objects.get(pk=id)
    materials = order.materials.all()
    materials_mass = []
    for m in materials:
        materials_mass.append(m.item.article)
    supplier_email = order.supplier.email
    SendTo(materials_mass, supplier_email, order.order.number)
    curr_state = order.status
    if curr_state == 0:
        order.status = 1
        order.save(update_fields=['status'])
    for mat in materials:
        mat_curr_state = mat.ordered
        if mat_curr_state == 0:
            mat.ordered = 1
            mat.ordered_icon = 1
            mat.save(update_fields=['ordered', 'ordered_icon'])
    return redirect('manager:order_view', id=order.order.pk)

@login_required(login_url='login')
def M_TextileOrder(request, id):
    qs = OrderItemTextile1.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 0:
        qs.ordered = 1
        qs.ordered_icon = 1
        qs.save(update_fields=['ordered', 'ordered_icon'])

    return redirect('manager:order_view', id=qs.order.pk)

@login_required(login_url='login')
def M_TextileOrdered(request, id):
    qs = OrderItemTextile1.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 1:
        qs.ordered = 2
        qs.ordered_icon = 2
        qs.save(update_fields=['ordered', 'ordered_icon'])

    offer = Offer.objects.get(order=qs.order)
    offer_version = offer.version.get_version_display()
    textile_all = OrderItemTextile1.objects.filter(order=qs.order, version=offer_version)
    textile_curr = textile_all.filter(ordered=2).count()


    if textile_curr == textile_all.count():
        curr_state = qs.order.textile_state
        if curr_state == 0:
            qs.order.textile_state = 1
            qs.order.save(update_fields=['textile_state'])

    M_ChangeOrderState(qs.order, 2, 5, 6)

    return redirect('manager:order_view', id=qs.order.pk)

@login_required(login_url='login')
def M_TextilePayed(request, id):
    qs = OrderItemTextile1.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 2:
        qs.ordered = 3
        qs.ordered_icon = 3
        qs.save(update_fields=['ordered', 'ordered_icon'])


    offer = Offer.objects.get(order=qs.order)
    offer_version = offer.version.get_version_display()
    textile_all = OrderItemTextile1.objects.filter(order=qs.order, version=offer_version)
    textile_curr = textile_all.filter(ordered=3).count()

    if textile_curr == textile_all.count():
        curr_state = qs.order.textile_state
        if curr_state == 1:
            qs.order.textile_state = 2
            qs.order.save(update_fields=['textile_state'])

    M_ChangeOrderState(qs.order, 3, 6, 7)

    return redirect('manager:order_view', id=qs.order.pk)

@login_required(login_url='login')
def M_TextileShipped(request, id):
    qs = OrderItemTextile1.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 3:
        qs.ordered = 4
        qs.ordered_icon = 4
        qs.save(update_fields=['ordered', 'ordered_icon'])

    offer = Offer.objects.get(order=qs.order)
    offer_version = offer.version.get_version_display()
    textile_all = OrderItemTextile1.objects.filter(order=qs.order, version=offer_version)
    textile_curr = textile_all.filter(ordered=4).count()


    if textile_curr == textile_all.count():
        curr_state = qs.order.textile_state
        if curr_state == 2:
            qs.order.textile_state = 3
            qs.order.save(update_fields=['textile_state'])

    M_ChangeOrderState(qs.order, 4, 7, 8)

    return redirect('manager:order_view', id=qs.order.pk)

@login_required(login_url='login')
def M_TextileStock(request, id):
    qs = OrderItemTextile1.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 0:
        qs.ordered = 4
        qs.ordered_icon = 4
        qs.save(update_fields=['ordered', 'ordered_icon'])
    M_ChangeOrderState(qs.order, 4, 7, 8)
    storage = StorageItemTextile.objects.get(item=qs.item)
    reserve = StorageItemTextileReserve.objects.get(order=qs.order, item=storage, quantity=qs.quantity)
    cat = PaymentCategory.objects.get(name='Отгрузка со склада')
    instance = Payment.objects.create(
        order=qs.order,
        category=cat,
        type_money=0,
        price=round(storage.price*qs.quantity, 2),
        receipt='Отгрузка со склада',
        user=request.user
    )
    storage.quantity = storage.quantity - qs.quantity
    storage.save(update_fields=['quantity'])
    reserve.delete()
    return redirect('manager:order_view', id=qs.order.pk)

@login_required(login_url='login')
def M_TextileStayOut(request, id):
    qs = OrderItemTextile1.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 1:
        qs.ordered = 6
        qs.ordered_icon = 6
        qs.save(update_fields=['ordered', 'ordered_icon'])
    return redirect('manager:order_view', id=qs.order.pk)

@login_required(login_url='login')
def SupplierCornice(request, id):
    item = OrderItemCornice.objects.get(pk=id)
    order = item.order
    supplier = item.item.manufacturer

    SuppOrder = SupplierOrderCornice.objects.filter(order=order, supplier=supplier).count()

    if SuppOrder > 0:
        check_SuppOrder = SupplierOrderCornice.objects.get(order=order, supplier=supplier)
        check_SuppOrder.materials.add(item)
    else:
        instance = SupplierOrderCornice.objects.create(order=order, supplier=supplier)
        instance.materials.add(item)

    # render(request, 'manager/index.html', context={})
    return redirect('manager:order_view', id=order.pk)

@login_required(login_url='login')
def M_CorniceOrder(request, id):
    qs = OrderItemCornice.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 0:
        qs.ordered = 1
        qs.ordered_icon = 1
        qs.save(update_fields=['ordered', 'ordered_icon'])

    return redirect('manager:order_view', id=qs.order.pk)

@login_required(login_url='login')
def M_CorniceOrdered(request, id):
    qs = OrderItemCornice.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 1:
        qs.ordered = 2
        qs.ordered_icon = 2
        qs.save(update_fields=['ordered', 'ordered_icon'])

    offer = Offer.objects.get(order=qs.order)
    offer_version = offer.version.get_version_display()
    cornice_all = OrderItemCornice.objects.filter(order=qs.order, version=offer_version)
    cornice_curr = cornice_all.filter(ordered=2).count()

    if cornice_curr == cornice_all.count():
        curr_state = qs.order.cornice_state
        if curr_state == 0:
            qs.order.cornice_state = 1
            qs.order.save(update_fields=['cornice_state'])

    M_ChangeOrderState(qs.order, 2, 5, 6)

    return redirect('manager:order_view', id=qs.order.pk)

@login_required(login_url='login')
def M_CornicePayed(request, id):
    qs = OrderItemCornice.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 2:
        qs.ordered = 3
        qs.ordered_icon = 3
        qs.save(update_fields=['ordered', 'ordered_icon'])


    offer = Offer.objects.get(order=qs.order)
    offer_version = offer.version.get_version_display()
    textile_all = OrderItemCornice.objects.filter(order=qs.order, version=offer_version)
    textile_curr = textile_all.filter(ordered=3).count()

    if textile_curr == textile_all.count():
        curr_state = qs.order.cornice_state
        if curr_state == 1:
            qs.order.cornice_state = 2
            qs.order.save(update_fields=['cornice_state'])

    M_ChangeOrderState(qs.order, 3, 6, 7)

    return redirect('manager:order_view', id=qs.order.pk)


@login_required(login_url='login')
def M_CorniceShipped(request, id):
    qs = OrderItemCornice.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 3:
        qs.ordered = 4
        qs.ordered_icon = 4
        qs.save(update_fields=['ordered', 'ordered_icon'])

    offer = Offer.objects.get(order=qs.order)
    offer_version = offer.version.get_version_display()
    textile_all = OrderItemCornice.objects.filter(order=qs.order, version=offer_version)
    textile_curr = textile_all.filter(ordered=4).count()

    if textile_curr == textile_all.count():
        curr_state = qs.order.cornice_state
        if curr_state == 2:
            qs.order.cornice_state = 3
            qs.order.save(update_fields=['cornice_state'])

    M_ChangeOrderState(qs.order, 4, 7, 8)

    return redirect('manager:order_view', id=qs.order.pk)


@login_required(login_url='login')
def M_CorniceStock(request, id):
    qs = OrderItemCornice.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 0:
        qs.ordered = 5
        qs.ordered_icon = 5
        qs.save(update_fields=['ordered', 'ordered_icon'])
    return redirect('manager:order_view', id=qs.order.pk)

@login_required(login_url='login')
def M_CorniceStayOut(request, id):
    qs = OrderItemCornice.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 1:
        qs.ordered = 6
        qs.ordered_icon = 6
        qs.save(update_fields=['ordered', 'ordered_icon'])
    return redirect('manager:order_view', id=qs.order.pk)

@login_required(login_url='login')
def M_SewingOrder(request, id):
    qs = OrderItemWorkSewing.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 0:
        qs.ordered = 1
        qs.ordered_icon = 1
        qs.save(update_fields=['ordered', 'ordered_icon'])

    M_ChangeWorkOrderState(qs.order)
    return redirect('manager:order_view', id=qs.order.pk)

@login_required(login_url='login')
def M_AssemblyOrder(request, id):
    qs = OrderItemWorkAssembly.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 0:
        qs.ordered = 1
        qs.ordered_icon = 1
        qs.save(update_fields=['ordered', 'ordered_icon'])

    M_ChangeWorkOrderState(qs.order)
    return redirect('manager:order_view', id=qs.order.pk)

@login_required(login_url='login')
def M_HangingOrder(request, id):
    qs = OrderItemWorkHanging.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 0:
        qs.ordered = 1
        qs.ordered_icon = 1
        qs.save(update_fields=['ordered', 'ordered_icon'])

    M_ChangeWorkOrderState(qs.order)
    return redirect('manager:order_view', id=qs.order.pk)

@login_required(login_url='login')
def M_DeliveryOrder(request, id):
    qs = OrderItemWorkDelivery.objects.get(pk=id)
    curr_state = qs.ordered
    if curr_state == 0:
        qs.ordered = 1
        qs.ordered_icon = 1
        qs.save(update_fields=['ordered', 'ordered_icon'])

    M_ChangeWorkOrderState(qs.order)
    return redirect('manager:order_view', id=qs.order.pk)

import datetime

@login_required(login_url='login')
def M_OrderReady(request, id):
    qs = Order.objects.get(pk=id)
    curr_state = qs.status
    if curr_state == 9 or curr_state == 8:
        qs.status = 10
        qs.status_css = 10
        qs.progress = 10
        qs.date_finished = datetime.datetime.now()
        qs.save(update_fields=['status', 'status_css', 'progress', 'date_finished'])
    return redirect('main:orders')


from itertools import chain
from operator import attrgetter

@login_required(login_url='login')
def M_SupplierOrders(request):
    qs = SupplierOrderedTextile.objects.all()
    qc = SupplierOrderedCornice.objects.all()
    result_list = sorted(
        chain(qs, qc),
        key=attrgetter('date_created'), reverse=True)
    return render(request, 'manager/supplier_orders.html', context={'orders': result_list})


@login_required(login_url='login')
def SupplierOrderSend2(request, id):

    if request.method == 'GET':
        order = SupplierOrder.objects.get(pk=id)
        materials = order.materials.all()
        materials_mass = []
        for m in materials:
            mat = f'{m.item.collection} {m.item.model} {m.item.color} в количестве ?x? метров'
            materials_mass.append(mat)

        return render(request, 'manager/supplier_send.html', context={'materials': materials_mass, 'supplier': order.supplier, 'order': order.order})
    if request.method == 'POST':
        order = SupplierOrder.objects.get(pk=id)
        materials = order.materials.all()
        email = request.POST['email']
        subject = request.POST['subject']
        text = request.POST['text']
        print(email, subject, text)

        SendTo(text, email, subject)
        curr_state = order.status
        if curr_state == 0:
            order.status = 1
            order.save(update_fields=['status'])
        for mat in materials:
            mat_curr_state = mat.ordered
            if mat_curr_state == 0:
                mat.ordered = 1
                mat.ordered_icon = 1
                mat.save(update_fields=['ordered', 'ordered_icon'])

        return redirect('manager:order_view', id=order.order.pk)
    return render(request, 'manager/supplier_send.html')

@login_required(login_url='login')
def M_TextileOrderedF(request, id):

    if request.method == 'GET':
        item = OrderItemTextile1.objects.get(pk=id)
        form = SupplierOrderedTextileForm({'order':item.order, 'item':item, 'status':0})
        return render(request, 'manager/add_textile_ordered.html',
                      context={'form': form,
                               'manufacturer': item.item.manufacturer.name,
                               'order': item.order.number,
                               'item': item})

    if request.method == 'POST':
        form = SupplierOrderedTextileForm(request.POST)
        order = request.POST.get("order", None)
        item = request.POST.get("item", None)
        price = request.POST.get("price", None)
        receipt = request.POST.get("receipt", None)
        status = request.POST.get("status", None)
        if order != None and item != None and price != None and receipt != None and status != None:
            order_id = Order.objects.get(pk=order)
            item_id = OrderItemTextile1.objects.get(pk=item)
            instance = SupplierOrderedTextile.objects.create(
                order=order_id,
                item=item_id,
                price=price,
                receipt=receipt,
                status=status
            )

            qs = item_id
            curr_state = qs.ordered
            if curr_state == 1:
                qs.ordered = 2
                qs.ordered_icon = 2
                qs.save(update_fields=['ordered', 'ordered_icon'])

            offer = Offer.objects.get(order=qs.order)
            offer_version = offer.version.get_version_display()
            textile_all = OrderItemTextile1.objects.filter(order=qs.order, version=offer_version)
            textile_curr = textile_all.filter(ordered=2).count()

            if textile_curr == textile_all.count():
                curr_state = qs.order.textile_state
                if curr_state == 0:
                    qs.order.textile_state = 1
                    qs.order.save(update_fields=['textile_state'])

            M_ChangeOrderState(qs.order, 2, 5, 6)

            return redirect('manager:order_view', id=order_id.pk)
        return render(request, 'manager/add_textile_ordered.html', context={'form': form})

@login_required(login_url='login')
def M_TextilePayedF(request, id):

    if request.method == 'GET':
        item = OrderItemTextile1.objects.get(pk=id)
        category = PaymentCategory.objects.get(name='Оплата поставщику')
        detail = SupplierOrderedTextile.objects.get(item=id)
        form = PaymentFormManager({'order': item.order, 'category': category, 'price': detail.price * item.quantity})
        return render(request, 'manager/payment_create.html',
                      context={'form': form, 'category': category, 'detail': detail, 'price': detail.price * item.quantity})

    if request.method == 'POST':
        item = OrderItemTextile1.objects.get(pk=id)
        form = PaymentFormManager(request.POST)
        category = request.POST.get("category", None)
        type_money = request.POST.get("type_money", None)
        price = request.POST.get("price", None)
        receipt = request.POST.get("receipt", None)
        if category != None and type_money != None and price != None and receipt != None:
            cat = PaymentCategory.objects.get(pk=category)
            instance = Payment.objects.create(
                order=item.order,
                category=cat,
                type_money=type_money,
                price=price,
                receipt=receipt,
                user=request.user
            )

            qs = OrderItemTextile1.objects.get(pk=id)
            curr_state = qs.ordered
            if curr_state == 2:
                qs.ordered = 3
                qs.ordered_icon = 3
                qs.save(update_fields=['ordered', 'ordered_icon'])

            offer = Offer.objects.get(order=qs.order)
            offer_version = offer.version.get_version_display()
            textile_all = OrderItemTextile1.objects.filter(order=qs.order, version=offer_version)
            textile_curr = textile_all.filter(ordered=3).count()

            if textile_curr == textile_all.count():
                curr_state = qs.order.textile_state
                if curr_state == 1:
                    qs.order.textile_state = 2
                    qs.order.save(update_fields=['textile_state'])

            M_ChangeOrderState(qs.order, 3, 6, 7)

            return redirect('manager:order_view', id=item.order.pk)
        return render(request, 'manager/payment_create.html', context={'form': form})

@login_required(login_url='login')
def SupplierOrderSend3(request, id):

    if request.method == 'GET':
        order = SupplierOrderCornice.objects.get(pk=id)
        materials = order.materials.all()
        materials_mass = []
        for m in materials:
            mat = f'{m.item.collection} {m.item.model} {m.item.long} в количестве ?x? метров'
            materials_mass.append(mat)

        return render(request, 'manager/supplier_send.html', context={'materials': materials_mass, 'supplier': order.supplier, 'order': order.order})
    if request.method == 'POST':
        order = SupplierOrderCornice.objects.get(pk=id)
        materials = order.materials.all()
        email = request.POST['email']
        subject = request.POST['subject']
        text = request.POST['text']
        print(email, subject, text)

        SendTo(text, email, subject)
        curr_state = order.status
        if curr_state == 0:
            order.status = 1
            order.save(update_fields=['status'])
        for mat in materials:
            mat_curr_state = mat.ordered
            if mat_curr_state == 0:
                mat.ordered = 1
                mat.ordered_icon = 1
                mat.save(update_fields=['ordered', 'ordered_icon'])

        return redirect('manager:order_view', id=order.order.pk)
    return render(request, 'manager/supplier_send.html')

@login_required(login_url='login')
def M_CorniceOrderedF(request, id):

    if request.method == 'GET':
        item = OrderItemCornice.objects.get(pk=id)
        form = SupplierOrderedCorniceForm({'order':item.order, 'item':item, 'status':0})
        return render(request, 'manager/add_textile_ordered.html',
                      context={'form': form,
                               'manufacturer': item.item.manufacturer.name,
                               'order': item.order.number,
                               'item': item})

    if request.method == 'POST':
        form = SupplierOrderedCorniceForm(request.POST)
        order = request.POST.get("order", None)
        item = request.POST.get("item", None)
        price = request.POST.get("price", None)
        receipt = request.POST.get("receipt", None)
        status = request.POST.get("status", None)
        if order != None and item != None and price != None and receipt != None and status != None:
            order_id = Order.objects.get(pk=order)
            item_id = OrderItemCornice.objects.get(pk=item)
            instance = SupplierOrderedCornice.objects.create(
                order=order_id,
                item=item_id,
                price=price,
                receipt=receipt,
                status=status
            )

            qs = item_id
            curr_state = qs.ordered
            if curr_state == 1:
                qs.ordered = 2
                qs.ordered_icon = 2
                qs.save(update_fields=['ordered', 'ordered_icon'])

            offer = Offer.objects.get(order=qs.order)
            offer_version = offer.version.get_version_display()
            textile_all = OrderItemCornice.objects.filter(order=qs.order, version=offer_version)
            textile_curr = textile_all.filter(ordered=2).count()

            if textile_curr == textile_all.count():
                curr_state = qs.order.cornice_state
                if curr_state == 0:
                    qs.order.cornice_state = 1
                    qs.order.save(update_fields=['cornice_state'])

            M_ChangeOrderState(qs.order, 2, 5, 6)

            return redirect('manager:order_view', id=order_id.pk)
        return render(request, 'manager/add_textile_ordered.html', context={'form': form})


@login_required(login_url='login')
def M_CornicePayedF(request, id):

    if request.method == 'GET':
        item = OrderItemCornice.objects.get(pk=id)
        category = PaymentCategory.objects.get(name='Оплата поставщику')
        detail = SupplierOrderedCornice.objects.get(item=id)
        form = PaymentFormManager({'order': item.order, 'category': category, 'price': detail.price * item.quantity})
        return render(request, 'manager/payment_create.html',
                      context={'form': form, 'category': category, 'detail': detail, 'price': detail.price * item.quantity})

    if request.method == 'POST':
        item = OrderItemCornice.objects.get(pk=id)
        form = PaymentFormManager(request.POST)
        category = request.POST.get("category", None)
        type_money = request.POST.get("type_money", None)
        price = request.POST.get("price", None)
        receipt = request.POST.get("receipt", None)
        if category != None and type_money != None and price != None and receipt != None:
            cat = PaymentCategory.objects.get(pk=category)
            instance = Payment.objects.create(
                order=item.order,
                category=cat,
                type_money=type_money,
                price=price,
                receipt=receipt,
                user=request.user
            )

            qs = OrderItemCornice.objects.get(pk=id)
            curr_state = qs.ordered
            if curr_state == 2:
                qs.ordered = 3
                qs.ordered_icon = 3
                qs.save(update_fields=['ordered', 'ordered_icon'])

            offer = Offer.objects.get(order=qs.order)
            offer_version = offer.version.get_version_display()
            textile_all = OrderItemCornice.objects.filter(order=qs.order, version=offer_version)
            textile_curr = textile_all.filter(ordered=3).count()

            if textile_curr == textile_all.count():
                curr_state = qs.order.cornice_state
                if curr_state == 1:
                    qs.order.cornice_state = 2
                    qs.order.save(update_fields=['cornice_state'])

            M_ChangeOrderState(qs.order, 3, 6, 7)

            return redirect('manager:order_view', id=item.order.pk)
        return render(request, 'manager/payment_create.html', context={'form': form})

@login_required(login_url='login')
def M_SewingPayedF(request, id):

    if request.method == 'GET':
        item = OrderItemWorkSewing.objects.get(pk=id)
        category = PaymentCategory.objects.get(name='Оплата за работы')
        form = PaymentFormManager({'order': item.order, 'category': category})
        return render(request, 'manager/payment_create_work.html',
                      context={'form': form, 'category': category, 'detail': item })

    if request.method == 'POST':
        item = OrderItemWorkSewing.objects.get(pk=id)
        form = PaymentFormManager(request.POST)
        category = request.POST.get("category", None)
        type_money = request.POST.get("type_money", None)
        price = request.POST.get("price", None)
        receipt = request.POST.get("receipt", None)
        if category != None and type_money != None and price != None and receipt != None:
            cat = PaymentCategory.objects.get(pk=category)
            instance = Payment.objects.create(
                order=item.order,
                category=cat,
                type_money=type_money,
                price=float(price)*item.quantity,
                receipt=receipt,
                user=request.user
            )

            qs = OrderItemWorkSewing.objects.get(pk=id)
            curr_state = qs.ordered
            if curr_state == 0:
                qs.ordered = 1
                qs.ordered_icon = 1
                qs.save(update_fields=['ordered', 'ordered_icon'])

            M_ChangeWorkOrderState(qs.order)

            return redirect('manager:order_view', id=qs.order.pk)
        return render(request, 'manager/payment_create_work.html', context={'form': form})

@login_required(login_url='login')
def M_AssemblyPayedF(request, id):

    if request.method == 'GET':
        item = OrderItemWorkAssembly.objects.get(pk=id)
        category = PaymentCategory.objects.get(name='Оплата за работы')
        form = PaymentFormManager({'order': item.order, 'category': category})
        return render(request, 'manager/payment_create_work.html',
                      context={'form': form, 'category': category, 'detail': item })

    if request.method == 'POST':
        item = OrderItemWorkAssembly.objects.get(pk=id)
        form = PaymentFormManager(request.POST)
        category = request.POST.get("category", None)
        type_money = request.POST.get("type_money", None)
        price = request.POST.get("price", None)
        receipt = request.POST.get("receipt", None)
        if category != None and type_money != None and price != None and receipt != None:
            cat = PaymentCategory.objects.get(pk=category)
            instance = Payment.objects.create(
                order=item.order,
                category=cat,
                type_money=type_money,
                price=float(price)*item.quantity,
                receipt=receipt,
                user=request.user
            )

            qs = OrderItemWorkAssembly.objects.get(pk=id)
            curr_state = qs.ordered
            if curr_state == 0:
                qs.ordered = 1
                qs.ordered_icon = 1
                qs.save(update_fields=['ordered', 'ordered_icon'])

            M_ChangeWorkOrderState(qs.order)

            return redirect('manager:order_view', id=qs.order.pk)
        return render(request, 'manager/payment_create_work.html', context={'form': form})

@login_required(login_url='login')
def M_HangingPayedF(request, id):

    if request.method == 'GET':
        item = OrderItemWorkHanging.objects.get(pk=id)
        category = PaymentCategory.objects.get(name='Оплата за работы')
        form = PaymentFormManager({'order': item.order, 'category': category})
        return render(request, 'manager/payment_create_work.html',
                      context={'form': form, 'category': category, 'detail': item })

    if request.method == 'POST':
        item = OrderItemWorkHanging.objects.get(pk=id)
        form = PaymentFormManager(request.POST)
        category = request.POST.get("category", None)
        type_money = request.POST.get("type_money", None)
        price = request.POST.get("price", None)
        receipt = request.POST.get("receipt", None)
        if category != None and type_money != None and price != None and receipt != None:
            cat = PaymentCategory.objects.get(pk=category)
            instance = Payment.objects.create(
                order=item.order,
                category=cat,
                type_money=type_money,
                price=float(price)*item.quantity,
                receipt=receipt,
                user=request.user
            )

            qs = OrderItemWorkHanging.objects.get(pk=id)
            curr_state = qs.ordered
            if curr_state == 0:
                qs.ordered = 1
                qs.ordered_icon = 1
                qs.save(update_fields=['ordered', 'ordered_icon'])

            M_ChangeWorkOrderState(qs.order)

            return redirect('manager:order_view', id=qs.order.pk)
        return render(request, 'manager/payment_create_work.html', context={'form': form})

@login_required(login_url='login')
def M_DeliveryPayedF(request, id):

    if request.method == 'GET':
        item = OrderItemWorkDelivery.objects.get(pk=id)
        category = PaymentCategory.objects.get(name='Оплата за работы')
        form = PaymentFormManager({'order': item.order, 'category': category})
        return render(request, 'manager/payment_create_work.html',
                      context={'form': form, 'category': category, 'detail': item })

    if request.method == 'POST':
        item = OrderItemWorkDelivery.objects.get(pk=id)
        form = PaymentFormManager(request.POST)
        category = request.POST.get("category", None)
        type_money = request.POST.get("type_money", None)
        price = request.POST.get("price", None)
        receipt = request.POST.get("receipt", None)
        if category != None and type_money != None and price != None and receipt != None:
            cat = PaymentCategory.objects.get(pk=category)
            instance = Payment.objects.create(
                order=item.order,
                category=cat,
                type_money=type_money,
                price=float(price)*item.quantity,
                receipt=receipt,
                user=request.user
            )

            qs = OrderItemWorkDelivery.objects.get(pk=id)
            curr_state = qs.ordered
            if curr_state == 0:
                qs.ordered = 1
                qs.ordered_icon = 1
                qs.save(update_fields=['ordered', 'ordered_icon'])

            M_ChangeWorkOrderState(qs.order)

            return redirect('manager:order_view', id=qs.order.pk)
        return render(request, 'manager/payment_create_work.html', context={'form': form})

@login_required(login_url='login')
def M_Sogl(request):
    qs = Order.objects.filter(discount_status=1).order_by('-date_created')
    customer = Customer.objects.all()
    context = {
        'orders': qs,
        'customer': customer
    }
    return render(request, 'manager/sogl.html', context)

@login_required(login_url='login')
def M_SoglView(request, id):
    qs = Order.objects.get(pk=id)
    curr_state = qs.discount_view
    if curr_state == 0:
        qs.discount_view = 1
        qs.save(update_fields=['discount_view'])

    sp = Room.objects.filter(order=qs, status=True)
    mass_dict = {}

    for q in sp:
        spec = Specification.objects.filter(room=q)
        sp_dict = {}
        for s in spec:
            spec_dict = {}
            textile_dict = []
            cornice_dict = []
            work_dict = []
            textile = OrderItemTextile1.objects.filter(specification=s)
            cornice = OrderItemCornice.objects.filter(specification=s)
            sewing = OrderItemWorkSewing.objects.filter(specification=s)
            assembly = OrderItemWorkAssembly.objects.filter(specification=s)
            hanging = OrderItemWorkHanging.objects.filter(specification=s)
            delivery = OrderItemWorkDelivery.objects.filter(specification=s)

            for t in textile:
                textile_mass = {
                    'item': f'{t.item.collection.name} {t.item.model} {t.item.color}',
                    'quantity': t.quantity,
                    'total': t.total_price(),
                    'discount_total': round(t.total_price() * qs.discount_t, 2),
                    'discount': round(t.total_price() - t.total_price() * qs.discount_t, 2),
                    'profit': round(t.total_price()-t.item.price_opt*t.quantity, 2),
                    'profit_d': round(t.total_price() * qs.discount_t - t.item.price_opt * t.quantity, 2),
                }
                textile_dict.append(textile_mass)
            for c in cornice:
                cornice_mass = {
                    'item': f'{c.item.collection.name} {c.item.model} {c.item.long}',
                    'quantity': c.quantity,
                    'total': c.total_price(),
                    'discount_total': round(c.total_price() * qs.discount_c, 2),
                    'discount': round(c.total_price() - c.total_price() * qs.discount_c, 2),
                    'profit': round(c.total_price()-c.item.price_opt*c.quantity, 2),
                    'profit_d': round(c.total_price() * qs.discount_c - c.item.price_opt * c.quantity, 2),
                }
                cornice_dict.append(cornice_mass)
            for sew in sewing:
                work_mass = {
                    'item': f'{sew.item.type_work.name}: {sew.item.name}',
                    'quantity': sew.quantity,
                    'total': sew.total_price(),
                    'discount_total': round(sew.total_price() * qs.discount_w, 2),
                    'discount': round(sew.total_price() - sew.total_price() * qs.discount_w, 2),
                    'profit': round(sew.total_price()-sew.item.price * sew.quantity, 2),
                    'profit_d': round(sew.total_price() * qs.discount_w - sew.item.price * sew.quantity, 2),
                }
                work_dict.append(work_mass)
            for ass in assembly:
                work_mass = {
                    'item': f'{ass.item.type_work.name}: {ass.item.name}',
                    'quantity': ass.quantity,
                    'total': ass.total_price(),
                    'discount_total': round(ass.total_price() * qs.discount_w, 2),
                    'discount': round(ass.total_price() - ass.total_price() * qs.discount_w, 2),
                    'profit': round(ass.total_price()-ass.item.price * ass.quantity, 2),
                    'profit_d': round(ass.total_price() * qs.discount_w - ass.item.price * ass.quantity, 2),
                }
                work_dict.append(work_mass)
            for han in hanging:
                work_mass = {
                    'item': f'{han.item.type_work.name}: {han.item.name}',
                    'quantity': han.quantity,
                    'total': han.total_price(),
                    'discount_total': round(han.total_price() * qs.discount_w, 2),
                    'discount': round(han.total_price() - han.total_price() * qs.discount_w, 2),
                    'profit': round(han.total_price()-han.item.price * han.quantity, 2),
                    'profit_d': round(han.total_price() * qs.discount_w - han.item.price * han.quantity, 2),
                }
                work_dict.append(work_mass)
            for han in delivery:
                work_mass = {
                    'item': f'{han.item.type_work.name}: {han.item.name}',
                    'quantity': han.quantity,
                    'total': han.total_price(),
                    'discount_total': round(han.total_price() * qs.discount_w, 2),
                    'discount': round(han.total_price() - han.total_price() * qs.discount_w, 2),
                    'profit': round(han.total_price()-han.item.price * han.quantity, 2),
                    'profit_d': round(han.total_price() * qs.discount_w - han.item.price * han.quantity, 2),
                }
                work_dict.append(work_mass)


            spec_dict[f'текстиль {s}'] = textile_dict
            spec_dict[f'карнизы {s}'] = cornice_dict
            spec_dict[f'работы {s}'] = work_dict

            sp_dict[s.get_version_display()] = spec_dict
        mass_dict[q.name] = sp_dict

    print(mass_dict)

    context = {
        'qs': qs,
        'room': sp,
        'mass': mass_dict
    }

    return render(request, 'manager/sogl_v.html', context)

@login_required(login_url='login')
def M_SoglSuccess(request, type_m, id):
    qs = Order.objects.get(pk=id)
    if type_m == '1':
        curr_state = qs.discount_t_s
        if curr_state == 1:
            qs.discount_t_s = 2
            qs.save(update_fields=['discount_t_s'])
    if type_m == '2':
        curr_state = qs.discount_c_s
        if curr_state == 1:
            qs.discount_c_s = 2
            qs.save(update_fields=['discount_c_s'])
    if type_m == '3':
        curr_state = qs.discount_w_s
        if curr_state == 1:
            qs.discount_w_s = 2
            qs.save(update_fields=['discount_w_s'])

    CheckDiscountState(id)

    return redirect('manager:sogl_view', id=qs.pk)

@login_required(login_url='login')
def M_SoglDeny(request,type_m, id):
    qs = Order.objects.get(pk=id)
    if type_m == '1':
        curr_state = qs.discount_t_s
        if curr_state == 1:
            qs.discount_t_s = 3
            qs.discount_t = 1
            qs.save(update_fields=['discount_t_s', 'discount_t'])
    if type_m == '2':
        curr_state = qs.discount_c_s
        if curr_state == 1:
            qs.discount_c_s = 3
            qs.discount_c = 1
            qs.save(update_fields=['discount_c_s', 'discount_c'])
    if type_m == '3':
        curr_state = qs.discount_w_s
        if curr_state == 1:
            qs.discount_w_s = 3
            qs.discount_w = 1
            qs.save(update_fields=['discount_w_s', 'discount_w'])

    CheckDiscountState(id)

    return redirect('manager:sogl_view', id=qs.pk)