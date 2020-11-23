from django.db import models
from django.shortcuts import reverse
from orders.models import Order, OrderItemTextile1, OrderItemCornice, OrderItemCorniceAdditional

class SupplierOrderedTextile(models.Model):
    ORDER_STATE = (
        (0, 'Не оплачено'),
        (1, 'Оплачено'),
    )
    type = models.CharField(verbose_name='Тип', max_length=100, default='Текстиль')
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(OrderItemTextile1, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Позиция')
    price = models.FloatField(verbose_name='Цена поставщика', max_length=100, default=0)
    receipt = models.CharField(verbose_name='Счет', max_length=100)
    status = models.IntegerField(verbose_name="Состояние заказа", choices=ORDER_STATE, default=0)
    date_shipped = models.CharField(verbose_name='Дата отгрузки', max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)

    def __str__(self):
        return str(self.order.number)

    def edit(self):
        return reverse('manager:supplier_ordered_textile_edit', kwargs={"id": self.pk})


class SupplierOrderedCornice(models.Model):
    ORDER_STATE = (
        (0, 'Не оплачено'),
        (1, 'Оплачено'),
    )

    type = models.CharField(verbose_name='Тип', max_length=100, default='Карнизы')
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(OrderItemCornice, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Позиция')
    additional = models.ForeignKey(OrderItemCorniceAdditional, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Позиция-доп')
    price = models.FloatField(verbose_name='Цена поставщика', max_length=100, default=0)
    receipt = models.CharField(verbose_name='Счет', max_length=100)
    status = models.IntegerField(verbose_name="Состояние заказа", choices=ORDER_STATE, default=0)
    date_shipped = models.CharField(verbose_name='Дата отгрузки', max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)

    def __str__(self):
        return str(self.order.number)

    def edit(self):
        return reverse('manager:supplier_ordered_cornice_edit', kwargs={"id": self.pk})
    def edit_additional(self):
        return reverse('manager:supplier_ordered_cornice_additional_edit', kwargs={"id": self.pk})