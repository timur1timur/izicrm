from django.db import models


class TypeWork(models.Model):
    name = models.CharField(verbose_name='Работы', max_length=100)

    def __str__(self):
        return self.name

class Work(models.Model):
    article = models.CharField(verbose_name='Артикул', max_length=100, blank=True)
    type_work = models.ForeignKey(TypeWork, null=True, on_delete=models.SET_NULL, verbose_name='Тип работ')
    name = models.CharField(verbose_name='Работы', max_length=100)
    price = models.FloatField(verbose_name='Стоимость')

    def __str__(self):
        return self.article

    def save(self, *args, **kwargs):
        self.article = str(self.type_work) + ': ' + str(self.name)
        super(Work, self).save(*args, **kwargs)
