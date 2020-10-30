from django.db import models
from django.utils.text import slugify
from .utils import transliterate
from django.shortcuts import reverse



class TextileManufact(models.Model):
    type_p = models.CharField(verbose_name='Тип', max_length=100, default='Текстиль')
    name = models.CharField(verbose_name='Производитель', max_length=100)
    email = models.EmailField(verbose_name='email', default='')
    phone = models.CharField(verbose_name='Телефон', max_length=100, blank=True, null=True)
    manager = models.CharField(verbose_name='Менеджер', max_length=100, blank=True, null=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = str(self.name).upper()
        super(TextileManufact, self).save(*args, **kwargs)


class TextileCollection(models.Model):
    name = models.CharField(verbose_name='Коллекция', max_length=100, blank=True)
    manufacturer = models.ForeignKey(TextileManufact, null=True, on_delete=models.CASCADE, verbose_name='Производитель', blank=True)

    def __str__(self):
        return str(self.name).upper()


#Ткани
class Textile(models.Model):
    article = models.CharField(verbose_name='Артикул', max_length=100, blank=True)
    manufacturer = models.ForeignKey(TextileManufact, null=True, on_delete=models.CASCADE, verbose_name='Производитель', blank=True)
    collection = models.ForeignKey(TextileCollection, null=True, on_delete=models.CASCADE, verbose_name='Коллекция')
    model = models.CharField(verbose_name='Модель', max_length=100)
    color = models.CharField(verbose_name='Цвет', max_length=100, default='')
    height = models.FloatField(verbose_name='Высота', null=True, blank=True)
    price_opt = models.FloatField(verbose_name='Цена отп', null=True, blank=True)
    price_pog = models.FloatField(verbose_name='Цена пог метра', null=True, blank=True)
    price_rul = models.FloatField(verbose_name='Цена рулон', null=True, blank=True)
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)

    def __str__(self):
        return self.article

    # def save(self, *args, **kwargs):
    #     self.article = slugify((str(self.collection.name) + "-" + self.model + "-" + self.color))
    #     super(Textile, self).save(*args, **kwargs)

    def choose_textile(self):
        return reverse('main:sp_add_textile', kwargs={"id": self.pk})


class CorniceManufact(models.Model):
    type_p = models.CharField(verbose_name='Тип', max_length=100, default='Карнизы')
    name = models.CharField(verbose_name='Производитель', max_length=100)
    email = models.EmailField(verbose_name='email', default='')
    phone = models.CharField(verbose_name='Телефон', max_length=100, blank=True, null=True)
    manager = models.CharField(verbose_name='Менеджер', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = str(self.name).upper()
        super(CorniceManufact, self).save(*args, **kwargs)

class CorniceCollection(models.Model):
    name = models.CharField(verbose_name='Коллекция', max_length=100, blank=True)
    manufacturer = models.ForeignKey(CorniceManufact, null=True, on_delete=models.CASCADE,
                                     verbose_name='Производитель', blank=True)

    def __str__(self):
        return str(self.name).upper()


#Корнизы
class Cornice(models.Model):
    article = models.CharField(verbose_name='Артикул', max_length=100, blank=True)
    manufacturer = models.ForeignKey(CorniceManufact, null=True, on_delete=models.SET_NULL, verbose_name='Производитель')
    collection = models.ForeignKey(CorniceCollection, null=True, on_delete=models.CASCADE, verbose_name='Коллекция')
    model = models.CharField(verbose_name='Модель', max_length=100)
    long = models.IntegerField(verbose_name='Длина, мм')
    price_opt = models.FloatField(verbose_name='Цена отп', null=True, blank=True)
    price_pog = models.FloatField(verbose_name='Цена пог метра', null=True, blank=True)
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)

    def __str__(self):
        return self.article

    def save(self, *args, **kwargs):
        manuf_tr = transliterate(str(self.collection))
        model_tr = transliterate(self.model)
        self.article = slugify(manuf_tr + "-" + model_tr + "-" + str(self.long))
        super(Cornice, self).save(*args, **kwargs)