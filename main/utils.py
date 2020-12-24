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
    return markup_full

def GetMarkupMaterialsStorage(order):
    cus = Customer.objects.get(order=order)
    markup_cus = MarkupCustomerCategory.objects.get(source_t=cus.source_t)
    markup_common = MarkupCommon.objects.get(id=1)
    markup_full = markup_cus.markup * markup_common.markup
    return markup_full


def GetMarkupWorks(order, type_item):
    cus = Customer.objects.get(order=order)
    markup_cus = MarkupCustomerCategory.objects.get(source_t=cus.source_t)
    markup_id = MarkupWorkCategory.objects.get(source_t=type_item)
    markup_common = MarkupCommon.objects.get(id=1)
    markup_full = markup_cus.markup * markup_id.markup * markup_common.markup
    return markup_full


import os
from orders.models import Offer, Room, Specification, OrderItemTextile1, OrderDoc, \
    OrderItemCornice, OrderItemWorkSewing, OrderItemWorkAssembly, OrderItemWorkHanging, OrderItemWorkDelivery, \
    OrderItemCorniceAdditional
import openpyxl
import convertapi
from os.path import join
from django.conf import settings
from docxtpl import DocxTemplate
import time

def delete_row_with_merged_ranges(sheet, idx):
    sheet.delete_rows(idx)
    for mcr in sheet.merged_cells:
        if idx < mcr.min_row:
            mcr.shift(row_shift=-1)
        elif idx <= mcr.max_row:
            mcr.shrink(bottom=1)

def find_value_sheet(col, value, sheet):
    start_v = 1
    while sheet[f'{col}{start_v}'].value != value:
        start_v += 1
    return start_v


def RemoveEmptyRow(col, start, stop, sheet):
    start_v = find_value_sheet(col, start, sheet) + 1
    finish_v = find_value_sheet(col, stop, sheet) - 1
    while sheet[f'{col}{start_v}'].value != stop:
        if sheet[f'{col}{start_v}'].value is None:
            delete_row_with_merged_ranges(sheet, start_v)
            finish_v -= 1
        else:
            start_v += 1

def GetContractP(id):
    time_start = time.time()
    order_id = Order.objects.get(pk=id)
    offer = Offer.objects.get(order=order_id)
    rooms = Room.objects.filter(order=order_id, status=1)
    id_doc = 1
    for room in rooms:
        wb = openpyxl.load_workbook(filename='contract_template2.xlsx')
        sheet = wb['template']
        sp = Specification.objects.get(order=order_id, room=room, version=offer.version.version)
        contract = Contract.objects.get(order=order_id)

        textile = OrderItemTextile1.objects.filter(specification=sp, order=order_id, version=offer.version.version)
        cornice = OrderItemCornice.objects.filter(specification=sp, order=order_id, version=offer.version.version)
        cornice_a = OrderItemCorniceAdditional.objects.filter(specification=sp, order=order_id, version=offer.version.version)
        sewing = OrderItemWorkSewing.objects.filter(specification=sp, order=order_id, version=offer.version.version)
        assembly = OrderItemWorkAssembly.objects.filter(specification=sp, order=order_id, version=offer.version.version)
        hanging = OrderItemWorkHanging.objects.filter(specification=sp, order=order_id, version=offer.version.version)
        delivery = OrderItemWorkDelivery.objects.filter(specification=sp, order=order_id, version=offer.version.version)

        room_value = 'C11'
        order_num = 'C2'
        order_full_name = 'J3'
        date_acceptance = 'C4'
        date_finish = 'C5'
        designer = 'C6'
        customer = 'C7'
        name_d = 'J2'
        comment1 = 'A14'
        comment2 = 'H14'

        total = 'C101'
        textile_t = 'F51'
        cornice_t = 'F81'
        sewing_t = 'L51'
        assembly_t = 'L81'
        hanging_t = 'L90'
        delivery_t = 'L98'

        discount_t = 'A52'
        discount_c = 'A82'
        discount_w_s = 'I52'
        discount_w_a = 'I82'
        discount_w_h = 'I91'
        discount_w_d = 'I99'

        sheet[comment1] = sp.comment1
        sheet[comment2] = sp.comment2


        sheet[total] = sp.total
        sheet[textile_t] = sp.textile_total
        sheet[cornice_t] = sp.cornice_total
        sheet[sewing_t] = sp.sewing_total
        sheet[assembly_t] = sp.assembly_total
        sheet[hanging_t] = sp.hanging_total
        sheet[delivery_t] = sp.delivery_total

        sheet[discount_t] = f'СКИДКА: {round(((1 - float(order_id.discount_t)) * 100),2)}%'
        sheet[discount_c] = f'СКИДКА: {round(((1 - float(order_id.discount_c)) * 100),2)}%'
        sheet[discount_w_s] = f'СКИДКА: {round(((1 - float(order_id.discount_w)) * 100),2)}%'
        sheet[discount_w_a] = f'СКИДКА: {round(((1 - float(order_id.discount_w)) * 100),2)}%'
        sheet[discount_w_h] = f'СКИДКА: {round(((1 - float(order_id.discount_w)) * 100),2)}%'
        sheet[discount_w_d] = f'СКИДКА: {round(((1 - float(order_id.discount_w)) * 100),2)}%'

        if order_id.discount_t == 1:
            sheet['A52'].value = None
            sheet['A53'].value = None
            sheet['C52'].value = None


        if order_id.discount_c == 1:
            sheet['A82'].value = None
            sheet['C82'].value = None
            sheet['A83'].value = None

        if order_id.discount_w == 1:
            sheet['I52'].value = None
            sheet['K52'].value = None
            sheet['I53'].value = None
            sheet['I82'].value = None
            sheet['K82'].value = None
            sheet['I83'].value = None
            sheet['I91'].value = None
            sheet['K91'].value = None
            sheet['I92'].value = None
            sheet['I99'].value = None
            sheet['K99'].value = None
            sheet['I100'].value = None

        contract_date = contract.date_created.strftime('%d.%m.%Y')

        sheet[room_value] = room.name
        sheet[order_num] = order_id.number
        sheet[order_full_name] = f'Договор № {order_id.number} от {contract_date}'
        sheet[date_acceptance] = contract.date_acceptance
        sheet[date_finish] = contract.date_finish
        sheet[designer] = order_id.user.get_full_name()
        sheet[customer] = contract.customer.name
        sheet[name_d] = f'Приложение {id_doc}'

        i = 25
        s_i = 25
        a_i = 55
        c_i = 55
        h_i = 85
        d_i = 94

        t_num = 1
        c_num = 1
        s_num = 1
        a_num = 1
        h_num = 1
        d_num = 1

        for t in textile:
            textile_num = f'A{i}'
            textile_model = f'C{i}'
            textile_color = f'D{i}'
            textile_price = f'F{i}'
            textile_type = f'E{i}'
            textile_total = f'H{i}'
            textile_quantity = f'G{i}'

            sheet[textile_num] = t_num
            sheet[textile_model] = f'{t.item.collection.name} {t.item.model}'
            sheet[textile_color] = t.item.color
            sheet[textile_price] = round(float(t.total_price())/float(t.quantity),2)
            sheet[textile_type] = t.item.type_i
            sheet[textile_quantity] = t.quantity
            sheet[textile_total] = t.total_price()

            i += 1
            t_num += 1

        for t in cornice:
            textile_num = f'A{c_i}'
            textile_model = f'C{c_i}'
            textile_color = f'D{c_i}'
            textile_price = f'F{c_i}'
            textile_type = f'E{c_i}'
            textile_total = f'H{c_i}'
            textile_quantity = f'G{c_i}'

            sheet[textile_num] = c_num
            sheet[textile_model] = f'{t.item.collection.name} {t.item.model}'
            sheet[textile_color] = t.item.long
            sheet[textile_price] = round(float(t.total_price())/float(t.quantity),2)
            sheet[textile_type] = 'шт.'
            sheet[textile_quantity] = t.quantity
            sheet[textile_total] = t.total_price()

            c_i += 1
            c_num += 1

        for s in sewing:
            sewing_num = f'I{s_i}'
            sewing_name = f'J{s_i}'
            sewing_price = f'K{s_i}'
            sewing_total = f'M{s_i}'
            sewing_quantity = f'L{s_i}'

            sheet[sewing_num] = s_num
            sheet[sewing_name] = s.item.name
            sheet[sewing_price] = round(float(s.total_price()) / float(s.quantity), 2)
            sheet[sewing_total] = s.total_price()
            sheet[sewing_quantity] = s.quantity
            s_i += 1
            s_num += 1

        for s in assembly:
            sewing_num = f'I{a_i}'
            sewing_name = f'J{a_i}'
            sewing_price = f'K{a_i}'
            sewing_total = f'M{a_i}'
            sewing_quantity = f'L{a_i}'

            sheet[sewing_num] = a_num
            sheet[sewing_name] = s.item.name
            sheet[sewing_price] = round(float(s.total_price()) / float(s.quantity), 2)
            sheet[sewing_total] = s.total_price()
            sheet[sewing_quantity] = s.quantity
            a_i += 1
            a_num += 1

        for s in hanging:
            sewing_num = f'I{h_i}'
            sewing_name = f'J{h_i}'
            sewing_price = f'K{h_i}'
            sewing_total = f'M{h_i}'
            sewing_quantity = f'L{h_i}'

            sheet[sewing_num] = h_num
            sheet[sewing_name] = s.item.name
            sheet[sewing_price] = round(float(s.total_price()) / float(s.quantity), 2)
            sheet[sewing_total] = s.total_price()
            sheet[sewing_quantity] = s.quantity
            h_i += 1
            h_num += 1

        for s in delivery:
            sewing_num = f'I{d_i}'
            sewing_name = f'J{d_i}'
            sewing_price = f'K{d_i}'
            sewing_total = f'M{d_i}'
            sewing_quantity = f'L{d_i}'

            sheet[sewing_num] = d_num
            sheet[sewing_name] = s.item.name
            sheet[sewing_price] = round(float(s.total_price()) / float(s.quantity), 2)
            sheet[sewing_total] = s.total_price()
            sheet[sewing_quantity] = s.quantity
            d_i += 1
            d_num += 1

        if textile.count() > sewing.count():
            RemoveEmptyRow('A','Ткани', 'Всего стоимость тканей:', sheet=sheet)
        else:
            RemoveEmptyRow('I','Пошив', 'Всего стоимость пошива:', sheet=sheet)

        if cornice.count() > assembly.count():
            RemoveEmptyRow('A', 'Карнизы', 'Всего стоимость карнизов:', sheet=sheet)
        else:
            RemoveEmptyRow('I', 'Монтаж', 'Всего стоимость монтажа:', sheet=sheet)

        RemoveEmptyRow('I', 'Развеска штор', 'Всего стоимость развески:', sheet=sheet)
        RemoveEmptyRow('I', 'Доставка', 'Всего стоимость доставки:', sheet=sheet)


        path = join(settings.MEDIA_ROOT, f'contract_{order_id.number}_Приложение{id_doc}.xlsx')
        # wb.save(f'media/contract_{order_id.number}_Приложение{id_doc}.xlsx')
        wb.save(path)
        wb.close()

        convertapi.api_secret = 'YrZSC1eLpGtaesdR'
        result = convertapi.convert('pdf', {'File': f'{path}', 'PdfResolution': '60'})
        name_pdf = f'contract_{order_id.number}_Приложение{id_doc}.pdf'
        result.file.save(f'{join(settings.MEDIA_ROOT, name_pdf)}')
        contract_file = OrderDoc.objects.get(order=order_id)
        if id_doc == 1:
            contract_file.contract_p1 = name_pdf
            contract_file.save(update_fields=['contract_p1'])
        elif id_doc == 2:
            contract_file.contract_p2 = name_pdf
            contract_file.save(update_fields=['contract_p2'])
        elif id_doc == 3:
            contract_file.contract_p3 = name_pdf
            contract_file.save(update_fields=['contract_p3'])
        os.remove(path)


        id_doc += 1
    time_finish = time.time()
    res_time = time_finish - time_start
    print(res_time)

def create_contract(id):
    order_id = Order.objects.get(pk=id)
    customer_id = Customer.objects.get(order=order_id)
    contract_id = Contract.objects.get(order=order_id)

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
    convertapi.api_secret = 'YrZSC1eLpGtaesdR'
    result = convertapi.convert('pdf', {'File': f'{path}'})
    name_pdf = f'contract_{order_id.number}.pdf'
    result.file.save(f'{join(settings.MEDIA_ROOT, name_pdf)}')
    contract_file = OrderDoc()
    contract_file.order = order_id
    contract_file.contract_doc.name = name_pdf
    contract_file.save()
    os.remove(path)
    if OrderDoc.objects.get(order=order_id):
        return 1
    else:
        return 0