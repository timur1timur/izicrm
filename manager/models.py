from django.db import models
from orders.models import Order, OrderItemTextile1, OrderItemCornice

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
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)

    def __str__(self):
        return str(self.order.number) + '_' + str(self.item.item.collection) + str(self.item.item.model) + '_' + str(self.item.quantity)


class SupplierOrderedCornice(models.Model):
    ORDER_STATE = (
        (0, 'Не оплачено'),
        (1, 'Оплачено'),
    )

    type = models.CharField(verbose_name='Тип', max_length=100, default='Карнизы')
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(OrderItemCornice, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Позиция')
    price = models.FloatField(verbose_name='Цена поставщика', max_length=100, default=0)
    receipt = models.CharField(verbose_name='Счет', max_length=100)
    status = models.IntegerField(verbose_name="Состояние заказа", choices=ORDER_STATE, default=0)
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)

    def __str__(self):
        return str(self.order.number) + '_' + str(self.item.item.collection) + str(self.item.item.model) + '_' + str(self.item.quantity)