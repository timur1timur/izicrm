from django.db import models
from materials.models import Cornice, Textile
from orders.models import Order


class StorageItemTextile(models.Model):
    item = models.ForeignKey(Textile, null=True, on_delete=models.CASCADE, verbose_name='Текстиль', )
    type_p = models.CharField(verbose_name='Тип', max_length=100, blank=True, null=True, default='Текстиль')
    quantity = models.FloatField(default=0, verbose_name='Количество')
    price = models.FloatField(verbose_name='Закупочная стоимость', default=0)
    price_f = models.FloatField(verbose_name='Цена фирмы', default=0)
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)

    def __str__(self):
        return str(self.item.article)

class StorageItemTextileReserve(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(StorageItemTextile, null=True, on_delete=models.CASCADE, verbose_name='Текстиль')
    quantity = models.FloatField(default=0, verbose_name='Количество')
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)

    def __str__(self):
        return str(self.order.number) + '-' + str(self.item) + '-' + str(self.quantity)


class StorageItemCornice(models.Model):
    item = models.ForeignKey(Cornice, null=True, on_delete=models.CASCADE, verbose_name='Карнизы', )
    type_p = models.CharField(verbose_name='Тип', max_length=100, blank=True, null=True, default='Карнизы')
    quantity = models.FloatField(default=0, verbose_name='Количество')
    reserve = models.FloatField(default=0, verbose_name='Резерв')
    price = models.FloatField(verbose_name='Закупочная стоимость', default=0)
    price_f = models.FloatField(verbose_name='Цена фирмы', default=0)
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)
    date_change = models.DateField(verbose_name='Дата изменения', blank=True, null=True)

    def __str__(self):
        return str(self.item.article)
