from django.db import models
from django.shortcuts import reverse


class MarkupCustomerCategory(models.Model):
    SOURCE_T = (
        (0, 'От Партнеров'),
        (1, 'Социальные сети'),
        (2, 'Маркетплейс'),
        (3, 'Телефон'),
        (4, 'Салон'),
    )
    source_t = models.IntegerField(verbose_name='Категория', choices=SOURCE_T, default=0)
    markup = models.FloatField(verbose_name='Наценка', max_length=100, default=1)

    def __str__(self):
        return self.get_source_t_display()


class MarkupMaterialCategory(models.Model):
    SOURCE_T = (
        (0, 'Текстиль'),
        (1, 'Карнизы'),
    )
    source_t = models.IntegerField(verbose_name='Категория', choices=SOURCE_T, default=0)
    markup = models.FloatField(verbose_name='Наценка', max_length=100, default=1)

    def __str__(self):
        return self.get_source_t_display()


class MarkupWorkCategory(models.Model):
    SOURCE_T = (
        (0, 'Пошив'),
        (1, 'Монтаж'),
        (2, 'Развеска штор'),
        (3, 'Доставка'),
    )
    source_t = models.IntegerField(verbose_name='Категория', choices=SOURCE_T, default=0)
    markup = models.FloatField(verbose_name='Наценка', max_length=100, default=1)

    def __str__(self):
        return self.get_source_t_display()


class MarkupCommon(models.Model):

    name = models.CharField(verbose_name='Название', max_length=100)
    markup = models.FloatField(verbose_name='Наценка', max_length=100, default=1)

    def __str__(self):
        return self.name

class MarkupSetting(models.Model):

    name = models.CharField(verbose_name='Название', max_length=100)
    value = models.IntegerField(verbose_name='Значение', default=0)

    def __str__(self):
        return self.name


class MarkupCurrency(models.Model):

    name = models.CharField(verbose_name='Название', max_length=100)
    value = models.FloatField(verbose_name='Значение', default=0)

    def __str__(self):
        return self.name