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


import os
from orders.models import Offer, Room, Specification, OrderItemTextile1, OrderDoc, \
    OrderItemCornice, OrderItemWorkSewing, OrderItemWorkAssembly, OrderItemWorkHanging, OrderItemWorkDelivery, \
    OrderItemCorniceAdditional
import openpyxl
import convertapi
from os.path import join
from django.conf import settings
from docxtpl import DocxTemplate


def delete_row_with_merged_ranges(sheet, idx):
    sheet.delete_rows(idx)
    for mcr in sheet.merged_cells:
        if idx < mcr.min_row:
            mcr.shift(row_shift=-1)
        elif idx <= mcr.max_row:
            mcr.shrink(bottom=1)


def GetContractP(id):
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
        c_i = 55

        t_num = 1
        c_num = 1
        s_num = 1


        for t in textile:
            textile_num = f'A{i}'
            textile_model = f'C{i}'
            textile_color = f'D{i}'
            textile_price = f'F{i}'
            textile_type = f'E{i}'
            textile_total = f'H{i}'
            textile_quantity = f'G{i}'

            sheet[textile_num] = t_num
            sheet[textile_model] = t.item.model
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

            sheet[textile_num] = t_num
            sheet[textile_model] = t.item.model
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


        i_check = 25
        i_fin = 50
        while sheet[f'A{i_check}'].value != 999:
            if sheet[f'A{i_check}'].value is None:
                delete_row_with_merged_ranges(sheet, i_check)
                print(f'Delete {i_check} row')
                i_fin -= 1
            else:
                print(f'{i_check} not empty')
                i_check += 1


        path = join(settings.MEDIA_ROOT, f'contract_{order_id.number}_Приложение{id_doc}.xlsx')
        # wb.save(f'media/contract_{order_id.number}_Приложение{id_doc}.xlsx')
        wb.save(path)
        wb.close()

        convertapi.api_secret = 'JP1PQL3pMArtbl1P'
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

    if OrderDoc.objects.get(order=order_id):
        return 1
    else:
        return 0

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
    convertapi.api_secret = 'JP1PQL3pMArtbl1P'
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