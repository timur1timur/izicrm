from django.urls import path
from .views import ReportOrders, ReportOrdersDate, ReportBudget, ReportBudgetMonth, ReportUser, ReportUserDate, \
    ReportSupplier, ReportSupplierDate


app_name = 'report'


urlpatterns = [
    path('orders/', ReportOrders, name="orders"),
    path('orders/<start>/<end>/', ReportOrdersDate, name="orders_date"),
    path('budget/', ReportBudget, name="budget"),
    path('budget/month/', ReportBudgetMonth, name="budget_month"),
    path('users/', ReportUser, name="users"),
    path('users/<start>/<end>/', ReportUserDate, name="users_date"),
    path('suppliers/', ReportSupplier, name="suppliers"),
    path('suppliers/<start>/<end>/', ReportSupplierDate, name="suppliers_date"),

]