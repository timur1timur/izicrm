from django.urls import path
from .views import ControlPayments, PaymentCreate, ControlPaymentsDate, UserList, UserCreate

app_name = 'director'


urlpatterns = [
    path('payments/list/', ControlPayments, name="payments_list"),
    path('payments/list/<start>/<end>/', ControlPaymentsDate, name="payments_list_date"),
    path('payments/create/', PaymentCreate, name="payment_create"),
    path('user/list/', UserList, name="user_list"),
    path('user/create/', UserCreate, name="user_create"),
]