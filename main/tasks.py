from celery.task import periodic_task
from datetime import timedelta
from manager.utils import CheckSupplierRe


@periodic_task(run_every=timedelta(seconds=30), name='my_check_task' )
def my_check_task():
    CheckSupplierRe()