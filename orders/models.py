from django.db import models
from .utils import decimal2text
from materials.models import Cornice, Textile, TextileManufact, CorniceManufact, CorniceAdditional, CorniceAdditionalOptions, CorniceCollectionColor
from works.models import Work
from django.shortcuts import reverse
from markup.models import MarkupMaterialCategory, MarkupWorkCategory
from django.contrib.auth.models import User

def GetCountOrder():
    last_number = Order.objects.all().order_by('id').last()
    if not last_number:
        return 'IZI0001'
    number_no = last_number.number
    new_number_no = str(int(number_no[4:]) + 1)
    new_number_no = number_no[0:-(len(new_number_no))] + new_number_no
    return new_number_no


class Order(models.Model):
    STATUS_V = (
        (0, 'Запланирован'),
        (1, 'КП подготовлено'),
        (2, 'КП утверждено'),
        (3, 'Договор подготовлен'),
        (4, 'Договор подписан'),
        (5, 'Аванс получен'),
        (6, 'Материалы заказаны'),
        (7, 'Материалы оплачены'),
        (8, 'Материалы отгружены'),
        (9, 'Работы заказаны'),
        (10, 'Заказ выдан'),
        (11, 'Архив'),

    )
    STATUS_CSS = (
        (0, 'secondary'),
        (1, 'secondary'),
        (2, 'secondary'),
        (3, 'info'),
        (4, 'info'),
        (5, 'primary'),
        (6, 'primary'),
        (7, 'primary'),
        (8, 'primary'),
        (9, 'primary'),
        (10, 'success'),
        (11, 'warning'),
    )
    STATUS_P = (
        (0, 0),
        (1, 10),
        (2, 20),
        (3, 30),
        (4, 40),
        (5, 50),
        (6, 60),
        (7, 70),
        (8, 80),
        (9, 90),
        (10, 100),
        (11, 0)
    )

    STATUS_V_T = (
        (0, 'Не заказаны'),
        (1, 'Заказаны'),
        (2, 'Оплачены'),
        (3, 'Отгружены'),
    )

    STATUS_V_D = (
        (0, 'Нет скидки'),
        (1, 'Не согласована'),
        (2, 'Согласована'),
        (3, 'Отказано'),
    )

    STATUS_V_D2 = (
        (0, 'Нет скидки'),
        (1, 'Ожидание согласования'),
        (2, 'Согласована'),
        (3, 'Отказано'),
        (4, 'Частичное согласование'),
    )

    number = models.CharField(verbose_name='Номер', max_length=100, blank=True, null=True, default=GetCountOrder)
    status = models.IntegerField(verbose_name='Статус', choices=STATUS_V, default=0)
    status_css = models.IntegerField(verbose_name='Статус', choices=STATUS_CSS, default=0)
    progress = models.IntegerField(verbose_name='Прогресс', choices=STATUS_P, default=0)
    textile_state = models.IntegerField(verbose_name='Состояние по текстилю', choices=STATUS_V_T, default=0)
    cornice_state = models.IntegerField(verbose_name='Состояние по карнизам', choices=STATUS_V_T, default=0)
    work_state = models.IntegerField(verbose_name='Состояние по работам', choices=STATUS_V_T, default=0)

    discount_status = models.IntegerField(verbose_name='Общий статус скидки', choices=STATUS_V_D2, default=0)
    discount_t = models.FloatField(verbose_name='Скидка к текстилю', max_length=100, blank=True, null=True, default=1)
    discount_t_s = models.IntegerField(verbose_name='Статус скидки', choices=STATUS_V_D, default=0)
    discount_c = models.FloatField(verbose_name='Скидка к карнизам', max_length=100, blank=True, null=True, default=1)
    discount_c_s = models.IntegerField(verbose_name='Статус скидки', choices=STATUS_V_D, default=0)
    discount_w = models.FloatField(verbose_name='Скидка к работам', max_length=100, blank=True, null=True, default=1)
    discount_w_s = models.IntegerField(verbose_name='Статус скидки', choices=STATUS_V_D, default=0)

    discount_view = models.IntegerField(verbose_name='Просмотр скидки', default=0)
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)
    date_finished = models.DateField(verbose_name='Дата исполнения', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
    user_view = models.IntegerField(verbose_name='Просмотр', default=0)


    def __str__(self):
        return self.number

    def get_absolute_url(self):
        return reverse('main:order_view', kwargs={"id": self.pk})

    def create_order(self):
        return reverse('main:order_create')

    def remove_order(self):
        return reverse('main:order_remove', kwargs={"id": self.pk})

    def create_sp(self):
        return reverse('main:specification_add', kwargs={"id": self.pk})

    def create_room(self):
        return reverse('main:room_add', kwargs={"id": self.pk})

    def create_kp(self):
        return reverse('main:order_kp', kwargs={"id": self.pk})

    def create_offer(self):
        return reverse('main:offer_create', kwargs={"id": self.pk})

    def create_customer(self):
        return reverse('main:customer_create', kwargs={"id": self.pk})

    def create_contract(self):
        return reverse('main:contract_create', kwargs={"id": self.pk})

    def create_contract_xls(self):
        return reverse('main:contract_create_xls', kwargs={"id": self.pk})

    def ready_contract(self):
        return reverse('main:contract_ready', kwargs={"id": self.pk})

    def get_doc(self):
        return reverse('main:contract_get', kwargs={"id": self.pk})

    def create_prepay(self):
        return reverse('main:prepay_create', kwargs={"id": self.pk})

    def ready_order(self):
        return reverse('common:order_ready', kwargs={"id": self.pk})

    def archive(self):
        return reverse('main:order_archive', kwargs={"id": self.pk})


class TrackedOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return str(self.order.number) + ' ' + str(self.user)


class Customer(models.Model):
    SOURCE_T = (
        (0, 'От Партнеров'),
        (1, 'Социальные сети'),
        (2, 'Маркетплейс'),
        (3, 'Телефон'),
        (4, 'Салон'),
    )
    order = models.ManyToManyField(Order, verbose_name='Заказ')
    name = models.CharField(verbose_name='ФИО', max_length=100)
    phone = models.CharField(verbose_name='Телефон', max_length=100, blank=True)
    email = models.CharField(verbose_name='email', max_length=100, blank=True)
    address = models.CharField(verbose_name='Адрес', max_length=300, blank=True)
    pass_series = models.CharField(verbose_name='Серия', max_length=10, blank=True)
    pass_number = models.CharField(verbose_name='Номер', max_length=10, blank=True)
    pass_date = models.CharField(verbose_name='Дата выдачи', max_length=10, blank=True)
    pass_issued = models.CharField(verbose_name='Выдан', max_length=300, blank=True)
    source_t = models.IntegerField(verbose_name='Источник', choices=SOURCE_T, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Contract(models.Model):
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Покупатель')
    number = models.CharField(verbose_name='Номер договора', max_length=100, blank=True)
    date = models.CharField(verbose_name='Дата договора', max_length=100, blank=True)
    price = models.FloatField(verbose_name='Стоимость', max_length=100)
    price_w = models.CharField(verbose_name='Стоимость прописью', max_length=500, blank=True)
    garant = models.IntegerField(verbose_name='Гарантийный срок)', default=1)
    prepay = models.IntegerField(verbose_name='Размер предоплаты')
    prepay_duration = models.IntegerField(verbose_name='Предоплата в течение')
    work_start = models.CharField(verbose_name='Начало работ (через)', default=5, max_length=100, blank=True, null=True)
    work_duration = models.CharField(verbose_name='Длительность работ', max_length=100, blank=True, null=True)
    date_acceptance = models.CharField(verbose_name='Дата приемки', max_length=100, blank=True, null=True)
    date_finish = models.CharField(verbose_name='Дата выполнения', max_length=100, blank=True)
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)
    state = models.CharField(verbose_name='Статус', max_length=100, blank=True)

    def save(self, *args, **kwargs):
        self.price_w = str(decimal2text(self.price)) + " рублей"
        self.number = self.order.number
        self.date = self.order.date_created.strftime('%d.%m.%Y')
        self.date_acceptance = self.order.date_created.strftime('%d.%m.%Y')
        super(Contract, self).save(*args, **kwargs)

    def __str__(self):
        return "Договор №" + self.number

class OrderDoc(models.Model):
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    contract_doc = models.FileField(blank=True, upload_to='contract')
    contract_p1 = models.FileField(blank=True, upload_to='contract')
    contract_p2 = models.FileField(blank=True, upload_to='contract')
    contract_p3 = models.FileField(blank=True, upload_to='contract')
    contract_p4 = models.FileField(blank=True, upload_to='contract')
    contract_p5 = models.FileField(blank=True, upload_to='contract')


class Room(models.Model):
    name = models.CharField(verbose_name='Название помещения', max_length=100, blank=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    status = models.BooleanField(verbose_name="Статус", max_length=1, blank=True, default=0)



    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('main:room', kwargs={"id": self.pk})

    def change_status(self):
        return reverse('main:room_status', kwargs={"id": self.pk})

    def ready(self):
        return reverse('main:room_ready', kwargs={"id": self.pk})

    def remove_room(self):
        return reverse('main:room_remove', kwargs={"id": self.pk})

    def create_sp(self):
        return reverse('main:specification_add', kwargs={"id": self.pk})


class Specification(models.Model):
    VERSION_ROOM = (
        ('Econom', 'Econom'),
        ('Standart', 'Standart'),
        ('Premium', 'Premium')
    )
    name = models.CharField(verbose_name='Название помещения', max_length=100, blank=True)
    version = models.CharField(verbose_name="Версия", max_length=10, choices=VERSION_ROOM, default='Econom')
    status = models.BooleanField(verbose_name="Статус", max_length=1, blank=True, default=0)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Помещение')
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    textile_total = models.CharField(verbose_name='Сумма текстиль', max_length=100, blank=True)
    cornice_total = models.CharField(verbose_name='Сумма корнизы', max_length=100, blank=True)
    sewing_total = models.CharField(verbose_name='Сумма пошив', max_length=100, blank=True)
    assembly_total = models.CharField(verbose_name='Сумма монтаж', max_length=100, blank=True)
    hanging_total = models.CharField(verbose_name='Сумма развеска', max_length=100, blank=True)
    delivery_total = models.CharField(verbose_name='Сумма доставка', max_length=100, blank=True)
    total = models.CharField(verbose_name='Общая сумма', max_length=100, blank=True)
    comment1 = models.CharField(verbose_name='Comment1', max_length=300, blank=True)
    comment2 = models.CharField(verbose_name='Comment1', max_length=300, blank=True)


    def __str__(self):
        return str(self.get_version_display())


    def get_absolute_url(self):
        return reverse('main:spec', kwargs={"pk": self.pk})

    def add_textile(self):
        return reverse('main:sp_add_textile', kwargs={"id": self.pk})

    def review_textile(self):
        return reverse('main:review_textile', kwargs={"id": self.pk})

    def review_cornice(self):
        return reverse('main:review_cornice', kwargs={"id": self.pk})

    def add_cornice(self):
        return reverse('main:sp_add_cornice', kwargs={"id": self.pk})

    def add_sewing(self):
        return reverse('main:sp_add_sewing', kwargs={"id": self.pk})

    def add_assembly(self):
        return reverse('main:sp_add_assembly', kwargs={"id": self.pk})

    def add_hanging(self):
        return reverse('main:sp_add_hanging', kwargs={"id": self.pk})

    def add_delivery(self):
        return reverse('main:sp_add_delivery', kwargs={"id": self.pk})

    def change_status(self):
        return reverse('main:change_status', kwargs={"id": self.pk})

    def ready(self):
        return reverse('main:sp_ready', kwargs={"id": self.pk})

    def copy_sp(self):
        return reverse('main:sp_copy', kwargs={"id": self.pk})

    def remove_sp(self):
        return reverse('main:sp_remove', kwargs={"id": self.pk})

class OfferVersion(models.Model):
    VERSION_OFFER = (
        ('Econom', 'Econom'),
        ('Standart', 'Standart'),
        ('Premium', 'Premium')
    )
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Помещение')
    version = models.CharField(verbose_name="Версия", max_length=10, choices=VERSION_OFFER, default='Econom')
    total = models.CharField(verbose_name='Общая сумма', max_length=100, blank=True)

    def __str__(self):
        return str(self.order.number) + '_' + str(self.version) + '_Total'

    def select_offer(self):
        return reverse('main:offer_select', kwargs={"id": self.pk})

class Offer(models.Model):
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    version = models.ForeignKey(OfferVersion, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Версия')

    def __str__(self):
        return str(self.version)


class PaymentCategory(models.Model):
    TYPE_P = (
        (0, 'Доход'),
        (1, 'Расход'),
    )


    name = models.CharField(verbose_name='Категория платежа', max_length=100, blank=True)
    type_p = models.IntegerField(verbose_name="Вид", choices=TYPE_P, default=0)

    def __str__(self):
        return self.name


class Payment(models.Model):
    TYPE_P = (
        (0, 'Доход'),
        (1, 'Расход'),
    )

    TYPE_PAYMENTS = (
        (0, 'Первичный аванс'),
        (1, 'Платеж'),
    )
    TYPE_MONEY = (
        (0, 'Безналичный'),
        (1, 'Наличный'),
    )

    name = models.CharField(verbose_name='Платеж', max_length=100, blank=True)
    category = models.ForeignKey(PaymentCategory, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Категория')
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Покупатель')
    type_money = models.IntegerField(verbose_name="Тип платежа", choices=TYPE_MONEY, default=0)
    price = models.FloatField(verbose_name="Сумма платежа", max_length=100, default=0)
    receipt = models.CharField(verbose_name='Чек', max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)


from markup.models import MarkupCurrency
from storage.models import StorageItemTextile

class OrderItemTextile1(models.Model):
    ORDER_STATE = (
        (0, 'Не заказан'),
        (1, 'Заказ отправлен'),
        (2, 'Заказан'),
        (3, 'Оплачен'),
        (4, 'Отгружены'),
        (5, 'В наличии'),
        (6, 'Отсутствует у поставщика'),
    )

    ORDER_STATE_ICON = (
        (0, 'fa-circle-thin'),
        (1, 'target'),
        (2, 'disc'),
        (3, 'dollar-sign'),
        (4, 'arrow-down-circle'),
        (5, 'arrow-down-circle'),
        (6, 'alert-circle'),
    )

    specification = models.ForeignKey(Specification, null=True, on_delete=models.CASCADE, verbose_name='Спецификация')
    version = models.CharField(verbose_name='Версия', max_length=100, blank=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(Textile, null=True, on_delete=models.CASCADE, verbose_name='Материал', )
    designation = models.CharField(verbose_name='Обозначение', max_length=100, blank=True)
    quantity = models.FloatField(default=1, verbose_name='Количество')
    markup = models.FloatField(verbose_name='Наценка', max_length=100, default=1)
    ordered = models.IntegerField(verbose_name="Состояние заказа", choices=ORDER_STATE, default=0)
    ordered_icon = models.IntegerField(verbose_name="Состояние заказа icon", choices=ORDER_STATE_ICON, default=0)


    def __str__(self):
        return str(self.item.article) + '-' + str(self.quantity)

    def save(self, *args, **kwargs):
        self.version = self.specification.get_version_display()
        self.designation = self.item.designation
        super(OrderItemTextile1, self).save(*args, **kwargs)

    def total_price(self):
        usd = MarkupCurrency.objects.get(name='USD')
        eur = MarkupCurrency.objects.get(name='EUR')
        m_textile = MarkupMaterialCategory.objects.get(source_t=0)

        storage = StorageItemTextile.objects.all().values_list('item', flat=True)
        if self.item.pk in storage:
            g_obj_price = StorageItemTextile.objects.get(item=self.item.pk)
            t_price = g_obj_price.price_f * self.quantity * (self.markup/m_textile.markup) * self.order.discount_t
        else:
            if self.item.currency == '$':
                t_price = self.item.price_opt * self.quantity * self.markup * self.order.discount_t * float(usd.value) * 1.03
            elif self.item.currency == 'euro':
                t_price = self.item.price_opt * self.quantity * self.markup * self.order.discount_t * float(eur.value) * 1.03
            else:
                t_price = self.item.price_opt * self.quantity * self.markup * self.order.discount_t
        return round(t_price, 2)

    def remove_textile(self):
        return reverse('main:sp_remove_textile', kwargs={"id": self.pk})

    def get_order(self):
        return reverse('manager:textile_ready', kwargs={"id": self.pk})

    def get_ordered(self):
        return reverse('manager:textile_ordered', kwargs={"id": self.pk})

    def get_payed(self):
        return reverse('manager:textile_payed', kwargs={"id": self.pk})

    def get_shipped(self):
        return reverse('manager:textile_shipped', kwargs={"id": self.pk})

    def get_stock(self):
        return reverse('manager:textile_stock', kwargs={"id": self.pk})

    def get_stay_out(self):
        return reverse('manager:textile_stay_out', kwargs={"id": self.pk})



class OrderItemCorniceAdditional(models.Model):
    ORDER_STATE = (
        (0, 'Не заказан'),
        (1, 'Заказ отправлен'),
        (2, 'Заказан'),
        (3, 'Оплачен'),
        (4, 'Отгружены'),
        (5, 'В наличии'),
        (6, 'Отсутствует у поставщика'),
    )

    ORDER_STATE_ICON = (
        (0, 'fa-circle-thin'),
        (1, 'target'),
        (2, 'disc'),
        (3, 'dollar-sign'),
        (4, 'arrow-down-circle'),
        (5, 'arrow-down-circle'),
        (6, 'alert-circle'),
    )

    specification = models.ForeignKey(Specification, null=True, on_delete=models.CASCADE, verbose_name='Спецификация')
    version = models.CharField(verbose_name='Версия', max_length=100, blank=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(CorniceAdditionalOptions, null=True, on_delete=models.CASCADE, verbose_name='Доп', )
    quantity = models.FloatField(default=1, verbose_name='Количество')
    color = models.ForeignKey(CorniceCollectionColor, null=True, on_delete=models.CASCADE, verbose_name='Цвет')
    markup = models.FloatField(verbose_name='Наценка', max_length=100, default=1)
    ordered = models.IntegerField(verbose_name="Состояние заказа", choices=ORDER_STATE, default=0)
    ordered_icon = models.IntegerField(verbose_name="Состояние заказа icon", choices=ORDER_STATE_ICON, default=0)

    def __str__(self):
        return str(self.item) + '-' + str(self.quantity)

    def save(self, *args, **kwargs):
        self.version = self.specification.get_version_display()
        super(OrderItemCorniceAdditional, self).save(*args, **kwargs)

    def total_price(self):
        t_price = self.item.price * self.quantity * self.markup * self.order.discount_c
        return round(t_price, 2)

    def get_order(self):
        return reverse('manager:cornice_additional_ready', kwargs={"id": self.pk})

    def get_ordered(self):
        return reverse('manager:cornice_additional_ordered', kwargs={"id": self.pk})

    def get_payed(self):
        return reverse('manager:cornice_additional_payed', kwargs={"id": self.pk})

    def get_shipped(self):
        return reverse('manager:cornice_additional_shipped', kwargs={"id": self.pk})

    def get_stock(self):
        return reverse('manager:cornice_additional_stock', kwargs={"id": self.pk})

    def get_stay_out(self):
        return reverse('manager:cornice_additional_stay_out', kwargs={"id": self.pk})

class OrderItemCornice(models.Model):
    ORDER_STATE = (
        (0, 'Не заказан'),
        (1, 'Заказ отправлен'),
        (2, 'Заказан'),
        (3, 'Оплачен'),
        (4, 'Отгружены'),
        (5, 'В наличии'),
        (6, 'Отсутствует у поставщика'),
    )

    ORDER_STATE_ICON = (
        (0, 'fa-circle-thin'),
        (1, 'target'),
        (2, 'disc'),
        (3, 'dollar-sign'),
        (4, 'arrow-down-circle'),
        (5, 'arrow-down-circle'),
        (6, 'alert-circle'),
    )

    specification = models.ForeignKey(Specification, null=True, on_delete=models.CASCADE, verbose_name='Спецификация')
    version = models.CharField(verbose_name='Версия', max_length=100, blank=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(Cornice, null=True, on_delete=models.CASCADE, verbose_name='Карнизы', )
    quantity = models.FloatField(default=1, verbose_name='Количество')
    markup = models.FloatField(verbose_name='Наценка', max_length=100, default=1)
    ordered = models.IntegerField(verbose_name="Состояние заказа", choices=ORDER_STATE, default=0)
    ordered_icon = models.IntegerField(verbose_name="Состояние заказа icon", choices=ORDER_STATE_ICON, default=0)

    def __str__(self):
        return str(self.item.article) + '-' + str(self.quantity)

    def save(self, *args, **kwargs):
        self.version = self.specification.get_version_display()
        super(OrderItemCornice, self).save(*args, **kwargs)

    def total_price(self):
        t_price = self.item.price_opt * self.quantity * self.markup * self.order.discount_c
        return round(t_price, 2)

    def remove_cornice(self):
        return reverse('main:sp_remove_cornice', kwargs={"id": self.pk})

    def get_order(self):
        return reverse('manager:cornice_ready', kwargs={"id": self.pk})

    def get_ordered(self):
        return reverse('manager:cornice_ordered', kwargs={"id": self.pk})

    def get_payed(self):
        return reverse('manager:cornice_payed', kwargs={"id": self.pk})

    def get_shipped(self):
        return reverse('manager:cornice_shipped', kwargs={"id": self.pk})

    def get_stock(self):
        return reverse('manager:cornice_stock', kwargs={"id": self.pk})

    def get_stay_out(self):
        return reverse('manager:cornice_stay_out', kwargs={"id": self.pk})


class OrderItemWorkSewing(models.Model):
    ORDER_STATE = (
        (0, 'Не заказан'),
        (1, 'Заказан'),
    )

    ORDER_STATE_ICON = (
        (0, 'fa-circle-thin'),
        (1, 'target'),
    )

    specification = models.ForeignKey(Specification, null=True, on_delete=models.CASCADE, verbose_name='Спецификация')
    version = models.CharField(verbose_name='Версия', max_length=100, blank=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(Work, null=True, on_delete=models.CASCADE, verbose_name='Работы', )
    quantity = models.FloatField(default=1, verbose_name='Количество')
    markup = models.FloatField(verbose_name='Наценка', max_length=100, default=1)
    ordered = models.IntegerField(verbose_name="Состояние заказа", choices=ORDER_STATE, default=0)
    ordered_icon = models.IntegerField(verbose_name="Состояние заказа icon", choices=ORDER_STATE_ICON, default=0)

    def __str__(self):
        return str(self.item.article) + '-' + str(self.quantity)

    def save(self, *args, **kwargs):
        self.version = self.specification.get_version_display()
        super(OrderItemWorkSewing, self).save(*args, **kwargs)

    def total_price(self):
        t_price = self.item.price * self.quantity * self.markup * self.order.discount_w
        return round(t_price, 2)

    def remove_sewing(self):
        return reverse('main:sp_remove_sewing', kwargs={"id": self.pk})

    def get_ordered(self):
        return reverse('manager:sewing_ordered', kwargs={"id": self.pk})


class OrderItemWorkAssembly(models.Model):
    ORDER_STATE = (
        (0, 'Не заказан'),
        (1, 'Заказан'),
    )

    ORDER_STATE_ICON = (
        (0, 'fa-circle-thin'),
        (1, 'target'),
    )

    specification = models.ForeignKey(Specification, null=True, on_delete=models.CASCADE, verbose_name='Спецификация')
    version = models.CharField(verbose_name='Версия', max_length=100, blank=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(Work, null=True, on_delete=models.CASCADE, verbose_name='Работы', )
    quantity = models.FloatField(default=1, verbose_name='Количество')
    markup = models.FloatField(verbose_name='Наценка', max_length=100, default=1)
    ordered = models.IntegerField(verbose_name="Состояние заказа", choices=ORDER_STATE, default=0)
    ordered_icon = models.IntegerField(verbose_name="Состояние заказа icon", choices=ORDER_STATE_ICON, default=0)

    def __str__(self):
        return str(self.item.article) + '-' + str(self.quantity)

    def save(self, *args, **kwargs):
        self.version = self.specification.get_version_display()
        super(OrderItemWorkAssembly, self).save(*args, **kwargs)

    def total_price(self):
        t_price = self.item.price * self.quantity * self.markup * self.order.discount_w
        return round(t_price, 2)

    def remove_assembly(self):
        return reverse('main:sp_remove_assembly', kwargs={"id": self.pk})

    def get_ordered(self):
        return reverse('manager:assembly_ordered', kwargs={"id": self.pk})


class OrderItemWorkHanging(models.Model):
    ORDER_STATE = (
        (0, 'Не заказан'),
        (1, 'Заказан'),
    )

    ORDER_STATE_ICON = (
        (0, 'fa-circle-thin'),
        (1, 'target'),
    )

    specification = models.ForeignKey(Specification, null=True, on_delete=models.CASCADE, verbose_name='Спецификация')
    version = models.CharField(verbose_name='Версия', max_length=100, blank=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(Work, null=True, on_delete=models.CASCADE, verbose_name='Работы', )
    quantity = models.FloatField(default=1, verbose_name='Количество')
    markup = models.FloatField(verbose_name='Наценка', max_length=100, default=1)
    ordered = models.IntegerField(verbose_name="Состояние заказа", choices=ORDER_STATE, default=0)
    ordered_icon = models.IntegerField(verbose_name="Состояние заказа icon", choices=ORDER_STATE_ICON, default=0)

    def __str__(self):
        return str(self.item.article) + '-' + str(self.quantity)

    def save(self, *args, **kwargs):
        self.version = self.specification.get_version_display()
        super(OrderItemWorkHanging, self).save(*args, **kwargs)

    def total_price(self):
        t_price = self.item.price * self.quantity * self.markup * self.order.discount_w
        return round(t_price, 2)

    def remove_hanging(self):
        return reverse('main:sp_remove_hanging', kwargs={"id": self.pk})

    def get_ordered(self):
        return reverse('manager:hanging_ordered', kwargs={"id": self.pk})


class OrderItemWorkDelivery(models.Model):
    ORDER_STATE = (
        (0, 'Не заказан'),
        (1, 'Заказан'),
    )

    ORDER_STATE_ICON = (
        (0, 'fa-circle-thin'),
        (1, 'target'),
    )

    specification = models.ForeignKey(Specification, null=True, on_delete=models.CASCADE, verbose_name='Спецификация')
    version = models.CharField(verbose_name='Версия', max_length=100, blank=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(Work, null=True, on_delete=models.CASCADE, verbose_name='Работы', )
    quantity = models.FloatField(default=1, verbose_name='Количество')
    markup = models.FloatField(verbose_name='Наценка', max_length=100, default=1)
    ordered = models.IntegerField(verbose_name="Состояние заказа", choices=ORDER_STATE, default=0)
    ordered_icon = models.IntegerField(verbose_name="Состояние заказа icon", choices=ORDER_STATE_ICON, default=0)

    def __str__(self):
        return str(self.item.article) + '-' + str(self.quantity)

    def save(self, *args, **kwargs):
        self.version = self.specification.get_version_display()
        super(OrderItemWorkDelivery, self).save(*args, **kwargs)

    def total_price(self):
        t_price = self.item.price * self.quantity * self.markup * self.order.discount_w
        return round(t_price, 2)

    def remove_delivery(self):
        return reverse('main:sp_remove_delivery', kwargs={"id": self.pk})

    def get_ordered(self):
        return reverse('manager:delivery_ordered', kwargs={"id": self.pk})


class SupplierOrder(models.Model):
    ORDER_STATE = (
        (0, 'Не отправлен'),
        (1, 'Отправлен'),
        (2, 'Получен ответ'),
    )

    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    supplier = models.ForeignKey(TextileManufact, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Поставщик')
    email = models.CharField(verbose_name='email', max_length=100, blank=True, null=True, default='')
    materials = models.ManyToManyField(OrderItemTextile1, verbose_name='Заказанный материал')

    status = models.IntegerField(verbose_name="Состояние заказа", choices=ORDER_STATE, default=0)

    def __str__(self):
        return str(self.supplier.name)

    def send_order(self):
        return reverse('manager:textile_send', kwargs={"id": self.pk})

    def send_check(self):
        return reverse('manager:order_send_check', kwargs={"id": self.pk})


class SupplierOrderCornice(models.Model):
    ORDER_STATE = (
        (0, 'Не отправлен'),
        (1, 'Отправлен'),
        (2, 'Получен ответ'),
    )

    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    supplier = models.ForeignKey(CorniceManufact, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Поставщик')
    email = models.CharField(verbose_name='email', max_length=100, blank=True, null=True, default='')
    materials = models.ManyToManyField(OrderItemCornice, verbose_name='Заказанный материал')
    additional = models.ManyToManyField(OrderItemCorniceAdditional, verbose_name='Заказанный доп материал')
    status = models.IntegerField(verbose_name="Состояние заказа", choices=ORDER_STATE, default=0)

    def __str__(self):
        return str(self.supplier.name)

    def send_order(self):
        return reverse('manager:cornice_send', kwargs={"id": self.pk})


class SupplierMail(models.Model):
    email = models.CharField(verbose_name='email', max_length=100, blank=True)
    subject = models.CharField(verbose_name='Тема письма', max_length=100, blank=True)
    text = models.CharField(verbose_name='Текст письма', max_length=1000, blank=True)
    type_p = models.CharField(verbose_name='Тип', max_length=1000, blank=True)

    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)

    def __str__(self):
        return str(self.supplier.name) + str(self.subject)



