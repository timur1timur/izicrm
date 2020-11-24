import smtplib
from email.mime.text import MIMEText
from time import sleep
from openpyxl import load_workbook
import os
import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
import datetime
from orders.models import SupplierOrder, Order
import imaplib


def send_email(addr_to, msg_subj, msg_text, files):
    addr_from = "zakaz@izidecor.ru"
    password  = "iz0dec0r"
    msg = MIMEMultipart()
    msg['From']    = addr_from
    msg['To']      = addr_to
    msg['Subject'] = msg_subj
    body = msg_text
    msg.attach(MIMEText(body, 'plain'))
    process_attachement(msg, files)
    server = smtplib.SMTP('smtp.yandex.ru', 587)
    server.starttls()
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()

def process_attachement(msg, files):                        # Функция по обработке списка, добавляемых к сообщению файлов
    for f in files:
        if os.path.isfile(f):                               # Если файл существует
            attach_file(msg,f)                              # Добавляем файл к сообщению
        elif os.path.exists(f):                             # Если путь не файл и существует, значит - папка
            dir = os.listdir(f)                             # Получаем список файлов в папке
            for file in dir:                                # Перебираем все файлы и...
                attach_file(msg,f+"/"+file)                 # ...добавляем каждый файл к сообщению

def attach_file(msg, filepath):                             # Функция по добавлению конкретного файла к сообщению
    filename = os.path.basename(filepath)                   # Получаем только имя файла
    ctype, encoding = mimetypes.guess_type(filepath)        # Определяем тип файла на основе его расширения
    if ctype is None or encoding is not None:               # Если тип файла не определяется
        ctype = 'application/octet-stream'                  # Будем использовать общий тип
    maintype, subtype = ctype.split('/', 1)                 # Получаем тип и подтип
    if maintype == 'text':                                  # Если текстовый файл
        with open(filepath) as fp:                          # Открываем файл для чтения
            file = MIMEText(fp.read(), _subtype=subtype)    # Используем тип MIMEText
            fp.close()                                      # После использования файл обязательно нужно закрыть
    elif maintype == 'image':                               # Если изображение
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'audio':                               # Если аудио
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
    else:                                                   # Неизвестный тип файла
        with open(filepath, 'rb') as fp:
            file = MIMEBase(maintype, subtype)              # Используем общий MIME-тип
            file.set_payload(fp.read())                     # Добавляем содержимое общего типа (полезную нагрузку)
            fp.close()
            encoders.encode_base64(file)                    # Содержимое должно кодироваться как Base64
    file.add_header('Content-Disposition', 'attachment', filename=filename) # Добавляем заголовки
    msg.attach(file)                                        # Присоединяем файл к сообщению


def SendTo(materials, supplier_email, order):
    sub = order
    textm = materials
    addr_to   = supplier_email
    files = []
    send_email(addr_to, sub, textm, files)


import imaplib
import email.header
import email

def mailanalytics(order1, email1):
    mail = imaplib.IMAP4_SSL('imap.yandex.ru')
    mail.login('timur1307timur@yandex.ru', 'K1r2m3v1307!')
    mail.select('INBOX')
    result, data = mail.uid('search', None, "ALL")
    latest_email_uid = data[0].split()
    mass1 = []
    mass2 = []
    mass3 = []
    for id in latest_email_uid:
        result, data = mail.uid('fetch', id, '(RFC822)')
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf8')
        email_message = email.message_from_string(raw_email_string)
        s1 = email_message['Subject']
        mass1.append(s1)
        s2 = email_message['From']
        mass2.append(s2)

        # if email_message.is_multipart():
        #     for payload in email_message.get_payload():
        #         if payload.get_content_maintype() == 'text':
        #             mass3.append(payload.get_payload(decode=True).decode('UTF8'))
        #
        # else:
        #     mass3.append(payload.get_payload(decode=True))



    mass_email = []
    mass_order = []
    i = 0
    while i < len(mass1):
        value_email = mass2[i].split(' ')[-1].replace('<','').replace('>','')
        mass_email.append(value_email)
        value_order = mass1[i].split(' ')[1].replace('\r', '').replace('\n', '')
        mass_order.append(value_order)
        i += 1

    my_dict = {}
    for i, j in zip(mass_order, mass_email):
        if i in my_dict:          # your `if` check
            my_dict[i].append(j)  # append value to existing list
        else:
            my_dict[i] = [j]

    flag = 0
    if my_dict.get(order1):
        for em in my_dict.get(order1):
            if em == email1:
                flag += 1
            else:
                flag += 0
    else:
        flag += 0

    if flag > 0:
        finish_flag = 1
    else:
        finish_flag = 0

    return finish_flag


from orders.models import Offer, OrderItemTextile1, OrderItemCornice, OrderItemCorniceAdditional


def M_StatusMaterialsCheck(order):
    offer = Offer.objects.get(order=order)
    offer_version = offer.version.get_version_display()
    textile_all = OrderItemTextile1.objects.filter(order=order, version=offer_version)
    cornice_all = OrderItemCornice.objects.filter(order=order, version=offer_version)
    additional_all = OrderItemCorniceAdditional.objects.filter(order=order, version=offer_version)
    return [textile_all.count(), cornice_all.count()+additional_all.count()]

def M_GetStatusMaterialOrder(order, state):
    offer = Offer.objects.get(order=order)
    offer_version = offer.version.get_version_display()
    textile_all = OrderItemTextile1.objects.filter(order=order, version=offer_version)
    cornice_all = OrderItemCornice.objects.filter(order=order, version=offer_version)
    additional_all = OrderItemCorniceAdditional.objects.filter(order=order, version=offer_version)
    textile_curr = textile_all.filter(ordered=state).count()
    textile_stock = textile_all.filter(ordered=5).count()
    cornice_curr = cornice_all.filter(ordered=state).count()
    cornice_stock = cornice_all.filter(ordered=5).count()
    additional_curr = additional_all.filter(ordered=state).count()
    additional_stock = additional_all.filter(ordered=5).count()

    textile_curr += textile_stock
    cornice_curr += (cornice_stock + additional_curr + additional_stock)

    return [textile_curr, cornice_curr]

def M_ChangeOrderState(order, state, state1, state2):
    state_m_textile = M_StatusMaterialsCheck(order)[0]
    state_m_order_textile = M_GetStatusMaterialOrder(order, state)[0]
    state_m_cornice = M_StatusMaterialsCheck(order)[1]
    state_m_order_cornice = M_GetStatusMaterialOrder(order, state)[1]


    if state_m_textile > 0 and state_m_cornice > 0:
        if state_m_order_textile == state_m_textile and state_m_order_cornice == state_m_cornice:
            if order.status == state1:
                order.status = state2
                order.status_css = state2
                order.progress = state2
                order.save(update_fields=['status', 'status_css', 'progress'])

    elif state_m_textile > 0 and state_m_cornice == 0:
        if state_m_order_textile == state_m_textile:
            if order.status == state1:
                order.status = state2
                order.status_css = state2
                order.progress = state2
                order.save(update_fields=['status', 'status_css', 'progress'])

    elif state_m_textile == 0 and state_m_cornice > 0:
        if state_m_order_cornice == state_m_cornice:
            if order.status == state1:
                order.status = state2
                order.status_css = state2
                order.progress = state2
                order.save(update_fields=['status', 'status_css', 'progress'])
    return print(f'Change status {order} in {state2}')

from orders.models import OrderItemWorkSewing, OrderItemWorkAssembly, OrderItemWorkHanging, OrderItemWorkDelivery


def M_StatusWorkCheck(order):
    offer = Offer.objects.get(order=order)
    offer_version = offer.version.get_version_display()
    sewing_all = OrderItemWorkSewing.objects.filter(order=order, version=offer_version).count()
    assembly_all = OrderItemWorkAssembly.objects.filter(order=order, version=offer_version).count()
    hanging_all = OrderItemWorkHanging.objects.filter(order=order, version=offer_version).count()
    delivery_all = OrderItemWorkDelivery.objects.filter(order=order, version=offer_version).count()
    return [sewing_all, assembly_all, hanging_all, delivery_all]

def M_GetStatusWorkOrder(order):
    offer = Offer.objects.get(order=order)
    offer_version = offer.version.get_version_display()
    sewing_all = OrderItemWorkSewing.objects.filter(order=order, version=offer_version)
    assembly_all = OrderItemWorkAssembly.objects.filter(order=order, version=offer_version)
    hanging_all = OrderItemWorkHanging.objects.filter(order=order, version=offer_version)
    delivery_all = OrderItemWorkDelivery.objects.filter(order=order, version=offer_version)
    sewing_curr = sewing_all.filter(ordered=1).count()
    assembly_curr = assembly_all.filter(ordered=1).count()
    hanging_curr = hanging_all.filter(ordered=1).count()
    delivery_curr = delivery_all.filter(ordered=1).count()
    return [sewing_curr, assembly_curr, hanging_curr, delivery_curr]

def M_ChangeWorkOrderState(order):
    s_sewing = M_StatusWorkCheck(order)[0]
    s_sewing_order = M_GetStatusWorkOrder(order)[0]
    s_assembly = M_StatusWorkCheck(order)[1]
    s_assembly_order = M_GetStatusWorkOrder(order)[1]
    s_hanging = M_StatusWorkCheck(order)[2]
    s_hanging_order = M_GetStatusWorkOrder(order)[2]
    s_delivery = M_StatusWorkCheck(order)[3]
    s_delivery_order = M_GetStatusWorkOrder(order)[3]

    if s_sewing > 0 and s_assembly > 0 and s_hanging > 0 and s_delivery > 0:
        if s_sewing == s_sewing_order and s_assembly == s_assembly_order and s_hanging == s_hanging_order and s_delivery == s_delivery_order:
            if order.status >= 5:
                order.status = 9
                order.status_css = 9
                order.progress = 9
                order.save(update_fields=['status', 'status_css', 'progress'])
    elif s_sewing == 0 and s_assembly > 0 and s_hanging > 0 and s_delivery > 0:
        if s_assembly == s_assembly_order and s_hanging == s_hanging_order and s_delivery == s_delivery_order:
            if order.status >= 5:
                order.status = 9
                order.status_css = 9
                order.progress = 9
                order.save(update_fields=['status', 'status_css', 'progress'])
    elif s_sewing > 0 and s_assembly == 0 and s_hanging > 0 and s_delivery > 0:
        if s_sewing == s_sewing_order and s_hanging == s_hanging_order and s_delivery == s_delivery_order:
            if order.status >= 5:
                order.status = 9
                order.status_css = 9
                order.progress = 9
                order.save(update_fields=['status', 'status_css', 'progress'])
    elif s_sewing > 0 and s_assembly > 0 and s_hanging == 0 and s_delivery > 0:
        if s_sewing == s_sewing_order and s_assembly == s_assembly_order and s_delivery == s_delivery_order:
            if order.status >= 5:
                order.status = 9
                order.status_css = 9
                order.progress = 9
                order.save(update_fields=['status', 'status_css', 'progress'])
    elif s_sewing > 0 and s_assembly > 0 and s_hanging > 0 and s_delivery == 0:
        if s_sewing == s_sewing_order and s_assembly == s_assembly_order and s_hanging == s_hanging_order:
            if order.status >= 5:
                order.status = 9
                order.status_css = 9
                order.progress = 9
                order.save(update_fields=['status', 'status_css', 'progress'])
    elif s_sewing > 0 and s_assembly == 0 and s_hanging == 0 and s_delivery == 0:
        if s_sewing == s_sewing_order:
            if order.status >= 5:
                order.status = 9
                order.status_css = 9
                order.progress = 9
                order.save(update_fields=['status', 'status_css', 'progress'])
    elif s_sewing == 0 and s_assembly > 0 and s_hanging == 0 and s_delivery == 0:
        if s_assembly == s_assembly_order:
            if order.status >= 5:
                order.status = 9
                order.status_css = 9
                order.progress = 9
                order.save(update_fields=['status', 'status_css', 'progress'])
    elif s_sewing == 0 and s_assembly == 0 and s_hanging > 0 and s_delivery == 0:
        if s_hanging == s_hanging_order:
            if order.status >= 5:
                order.status = 9
                order.status_css = 9
                order.progress = 9
                order.save(update_fields=['status', 'status_css', 'progress'])
    elif s_sewing == 0 and s_assembly == 0 and s_hanging == 0 and s_delivery > 0:
        if s_delivery == s_delivery_order:
            if order.status >= 5:
                order.status = 9
                order.status_css = 9
                order.progress = 9
                order.save(update_fields=['status', 'status_css', 'progress'])
    elif s_sewing > 0 and s_assembly > 0 and s_hanging == 0 and s_delivery == 0:
        if s_sewing == s_sewing_order and s_assembly == s_assembly_order:
            if order.status >= 5:
                order.status = 9
                order.status_css = 9
                order.progress = 9
                order.save(update_fields=['status', 'status_css', 'progress'])
    elif s_sewing > 0 and s_assembly == 0 and s_hanging > 0 and s_delivery == 0:
        if s_sewing == s_sewing_order and s_hanging == s_hanging_order:
            if order.status >= 5:
                order.status = 9
                order.status_css = 9
                order.progress = 9
                order.save(update_fields=['status', 'status_css', 'progress'])
    elif s_sewing > 0 and s_assembly == 0 and s_hanging == 0 and s_delivery > 0:
        if s_sewing == s_sewing_order and s_delivery == s_delivery_order:
            if order.status >= 5:
                order.status = 9
                order.status_css = 9
                order.progress = 9
                order.save(update_fields=['status', 'status_css', 'progress'])
    elif s_sewing == 0 and s_assembly > 0 and s_hanging > 0 and s_delivery == 0:
        if s_assembly == s_assembly_order and s_hanging == s_hanging_order:
            if order.status >= 5:
                order.status = 9
                order.status_css = 9
                order.progress = 9
                order.save(update_fields=['status', 'status_css', 'progress'])
    elif s_sewing == 0 and s_assembly > 0 and s_hanging == 0 and s_delivery > 0:
        if s_assembly == s_assembly_order and s_delivery == s_delivery_order:
            if order.status >= 5:
                order.status = 9
                order.status_css = 9
                order.progress = 9
                order.save(update_fields=['status', 'status_css', 'progress'])

    elif s_sewing == 0 and s_assembly == 0 and s_hanging > 0 and s_delivery > 0:
        if s_hanging == s_hanging_order and s_delivery == s_delivery_order:
            if order.status >= 5:
                order.status = 9
                order.status_css = 9
                order.progress = 9
                order.save(update_fields=['status', 'status_css', 'progress'])
    return print(f'Change status {order} in 9')


def CheckDiscountState(order):
    qs = Order.objects.get(pk=order)

    textile = qs.discount_t_s
    cornice = qs.discount_c_s
    work = qs.discount_w_s

    if textile > 0 and cornice > 0 and work > 0:
        if textile == 2 and cornice == 2 and work == 2:
            qs.discount_status = 2
            qs.save(update_fields=['discount_status'])
        if textile == 3 and cornice == 3 and work == 3:
            qs.discount_status = 3
            qs.discount_view = 0
            qs.save(update_fields=['discount_status'])
        if textile == 2 and cornice == 3 and work == 3:
            qs.discount_status = 4
            qs.save(update_fields=['discount_status'])
        if textile == 3 and cornice == 2 and work == 3:
            qs.discount_status = 4
            qs.save(update_fields=['discount_status'])
        if textile == 3 and cornice == 3 and work == 2:
            qs.discount_status = 4
            qs.save(update_fields=['discount_status'])
        if textile == 3 and cornice == 2 and work == 2:
            qs.discount_status = 4
            qs.save(update_fields=['discount_status'])
        if textile == 2 and cornice == 3 and work == 2:
            qs.discount_status = 4
            qs.save(update_fields=['discount_status'])
        if textile == 2 and cornice == 2 and work == 3:
            qs.discount_status = 4
            qs.save(update_fields=['discount_status'])
    elif textile == 0 and cornice > 0 and work > 0:
        if cornice == 2 and work == 2:
            qs.discount_status = 2
            qs.save(update_fields=['discount_status'])
        if cornice == 3 and work == 3:
            qs.discount_status = 3
            qs.discount_view = 0
            qs.save(update_fields=['discount_status'])
        if cornice == 2 and work == 3:
            qs.discount_status = 4
            qs.save(update_fields=['discount_status'])
        if cornice == 3 and work == 2:
            qs.discount_status = 4
            qs.save(update_fields=['discount_status'])
    elif textile > 0 and cornice == 0 and work > 0:
        if textile == 2 and work == 2:
            qs.discount_status = 2
            qs.save(update_fields=['discount_status'])
        if textile == 3 and work == 3:
            qs.discount_status = 3
            qs.discount_view = 0
            qs.save(update_fields=['discount_status'])
        if textile == 2 and work == 3:
            qs.discount_status = 4
            qs.save(update_fields=['discount_status'])
        if textile == 3 and work == 2:
            qs.discount_status = 4
            qs.save(update_fields=['discount_status'])
    elif textile > 0 and cornice > 0 and work == 0:
        if textile == 2 and cornice == 2:
            qs.discount_status = 2
            qs.save(update_fields=['discount_status'])
        if textile == 3 and cornice == 3:
            qs.discount_status = 3
            qs.discount_view = 0
            qs.save(update_fields=['discount_status'])
        if textile == 2 and cornice == 3:
            qs.discount_status = 4
            qs.save(update_fields=['discount_status'])
        if textile == 3 and cornice == 2:
            qs.discount_status = 4
            qs.save(update_fields=['discount_status'])
    elif textile > 0 and cornice == 0 and work == 0:
        if textile == 2:
            qs.discount_status = 2
            qs.save(update_fields=['discount_status'])
        if textile == 3:
            qs.discount_status = 3
            qs.discount_view = 0
            qs.save(update_fields=['discount_status'])
    elif textile == 0 and cornice > 0 and work == 0:
        if cornice == 2:
            qs.discount_status = 2
            qs.save(update_fields=['discount_status'])
        if cornice == 3:
            qs.discount_status = 3
            qs.discount_view = 0
            qs.save(update_fields=['discount_status'])
    elif textile == 0 and cornice == 0 and work > 0:
        if work == 2:
            qs.discount_status = 2
            qs.save(update_fields=['discount_status'])
        if work == 3:
            qs.discount_status = 3
            qs.discount_view = 0
            qs.save(update_fields=['discount_status'])