from django.urls import path
from .views import CustomerList, CustomerCreate, TextileManufactList, TextileManufactAdd, \
    CorniceManufactAdd, TextileList, TextileAdd, CorniceList, CorniceAdd, \
    TextileCollectionAdd, CorniceCollectionAdd, PaymentsList, PaymentCreate, ReportOrders, dashboard_designer, \
    dashboard_designer_date, dashboard_manager, dashboard_manager_date, TextileManufactEdit, CorniceManufactEdit, \
    TextileEdit, CorniceEdit, TextileRemove, CorniceRemove, TextileManufactRemove, CorniceManufactRemove, WorksList, \
    WorksAdd, WorksRemove, WorksEdit, TextileListFilter, CorniceAdditionalView, CorniceAdditionalList, \
    CorniceAdditionalDelete, CorniceAdditionalEdit

app_name = 'common'


urlpatterns = [

    path('customers/list/', CustomerList, name="customers_list"),
    path('customers/create/', CustomerCreate, name="customer_create"),
    path('payments/list/', PaymentsList, name="payments_list"),
    path('payments/create/', PaymentCreate, name="payment_create"),

    path('works/list/', WorksList, name="works_list"),
    path('works/create/', WorksAdd, name="works_create"),
    path('works/edit/<id>/', WorksEdit, name="works_edit"),
    path('works/remove/<id>/', WorksRemove, name="works_remove"),

    path('manufacturer/textile/list/', TextileManufactList, name="manufacturer_textile"),
    path('manufacturer/textile/add/', TextileManufactAdd, name="manufacturer_textile_add"),
    path('manufacturer/cornice/add/', CorniceManufactAdd, name="manufacturer_cornice_add"),
    path('manufacturer/textile/edit/<id>/', TextileManufactEdit, name="manufacturer_textile_edit"),
    path('manufacturer/cornice/edit/<id>/', CorniceManufactEdit, name="manufacturer_cornice_edit"),
    path('manufacturer/textile/remove/<id>/', TextileManufactRemove, name="manufacturer_textile_remove"),
    path('manufacturer/cornice/remove/<id>/', CorniceManufactRemove, name="manufacturer_cornice_remove"),

    path('collection/textile/add/', TextileCollectionAdd, name="collection_textile_add"),
    path('collection/cornice/add/', CorniceCollectionAdd, name="collection_cornice_add"),


    path('textile/list/', TextileList, name="textile_list"),
    path('textile/filter/<collection_id>/<model_id>/', TextileListFilter, name="textile_filter"),
    path('textile/add/', TextileAdd, name="textile_add"),
    path('textile/edit/<id>/', TextileEdit, name="textile_edit"),
    path('textile/remove/<id>/', TextileRemove, name="textile_remove"),

    path('cornice/list/', CorniceList, name="cornice_list"),
    path('cornice/add/', CorniceAdd, name="cornice_add"),
    path('cornice/edit/<id>/', CorniceEdit, name="cornice_edit"),
    path('cornice/remove/<id>/', CorniceRemove, name="cornice_remove"),

    path('cornice/additional/<id>/', CorniceAdditionalView, name="cornice_additional"),
    path('cornice/additional/edit/<id>/', CorniceAdditionalEdit, name="cornice_additional_edit"),
    path('cornice/additional/remove/<id>/', CorniceAdditionalDelete, name="cornice_additional_remove"),
    path('cornice/additional/list/<id>/', CorniceAdditionalList, name="cornice_additional_list"),



    path('report/orders/', ReportOrders, name='report_orders'),


    path('dashboard/designer/', dashboard_designer, name="dashboard_designer"),
    path('dashboard/designer/<start>/<end>/', dashboard_designer_date, name="dashboard_designer_date"),
    path('dashboard/manager/', dashboard_manager, name="dashboard_manager"),
    path('dashboard/manager/<start>/<end>/', dashboard_manager_date, name="dashboard_manager_date"),
]