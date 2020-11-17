from celery.task import periodic_task
from datetime import timedelta
from common.utils import get_currency_now
from markup.models import MarkupCurrency



@periodic_task(run_every=timedelta(minutes=60), name='get_currency')
def get_currency():
    currency = get_currency_now()
    print(currency)
    usd_base = MarkupCurrency.objects.get(name='USD')
    usd_base.value = currency['usd']
    usd_base.save(update_fields=['value'])
    eur_base = MarkupCurrency.objects.get(name='EUR')
    eur_base.value = currency['eur']
    eur_base.save(update_fields=['value'])

