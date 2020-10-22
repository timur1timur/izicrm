from django.urls import path
from .views import CustomerList, CustomerCreate, TextileManufactList, TextileManufactAdd, \
    CorniceManufactList, CorniceManufactAdd, TextileList, TextileAdd, CorniceList, CorniceAdd, \
    TextileCollectionAdd, CorniceCollectionAdd, PaymentsList, PaymentCreate, ReportOrders, dashboard_designer, \
    dashboard_designer_date, dashboard_manager, dashboard_manager_date

app_name = 'common'


urlpatterns = [

    path('customers/list/', CustomerList, name="customers_list"),
    path('customers/create/', CustomerCreate, name="customer_create"),
    path('payments/list/', PaymentsList, name="payments_list"),
    path('payments/create/', PaymentCreate, name="payment_create"),

    path('manufacturer/textile/list/', TextileManufactList, name="manufacturer_textile"),
    path('manufacturer/textile/add/', TextileManufactAdd, name="manufacturer_textile_add"),
    path('manufacturer/cornice/list/', CorniceManufactList, name="manufacturer_cornice"),
    path('manufacturer/cornice/add/', CorniceManufactAdd, name="manufacturer_cornice_add"),
    path('collection/textile/add/', TextileCollectionAdd, name="collection_textile_add"),
    path('collection/cornice/add/', CorniceCollectionAdd, name="collection_cornice_add"),
    path('textile/list/', TextileList, name="textile_list"),
    path('textile/add/', TextileAdd, name="textile_add"),
    path('cornice/list/', CorniceList, name="cornice_list"),
    path('cornice/add/', CorniceAdd, name="cornice_add"),
    path('report/orders/', ReportOrders, name='report_orders'),


    path('dashboard/designer/', dashboard_designer, name="dashboard_designer"),
    path('dashboard/designer/<start>/<end>/', dashboard_designer_date, name="dashboard_designer_date"),
    path('dashboard/manager/', dashboard_manager, name="dashboard_manager"),
    path('dashboard/manager/<start>/<end>/', dashboard_manager_date, name="dashboard_manager_date"),
]