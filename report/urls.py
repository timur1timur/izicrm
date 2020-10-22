from django.urls import path
from .views import ReportOrders, ReportOrdersDate, ReportBudget, ReportBudgetMonth, ReportUser


app_name = 'report'


urlpatterns = [
    path('orders/', ReportOrders, name="orders"),
    path('orders/<start>/<end>/', ReportOrdersDate, name="orders_date"),
    path('budget/', ReportBudget, name="budget"),
    path('budget/month/', ReportBudgetMonth, name="budget_month"),
    path('users/', ReportUser, name="users"),

]