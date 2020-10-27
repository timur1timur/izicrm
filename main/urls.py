from django.urls import path
from .views import  SpecificationTextileAdd, SpecificationViewD, \
    SpecificationCorniceAdd, SpecificationTextileRemove, SpecificationCorniceRemove, SpecificationSewingAdd, \
    SpecificationSewingRemove, SpecificationChangeStatus, SpecificationAssemblyAdd, SpecificationAssemblyRemove, \
    OrderCreate, OrderView, OrderRemove, OrderViewD, SpecificationAdd, SpecificationRemove, SpecificationReady, Test, \
    OrderCreateKp, RoomAdd, RoomRemove, RoomChangeStatus, RoomReady, ContractCreateXls, CustomerCreate, \
    ContractCreate, OfferCreate, OfferSelect, ContractCreateWord, GetContract, PaymentCreate, ContractReady, TestTemplate,\
    OrderCreateCustomer, SpecificationCopy, TextileReview, CorniceReview, SpecificationHangingAdd, SpecificationDeliveryAdd, \
    SpecificationHangingRemove, SpecificationDeliveryRemove, OrderArchive, GetDiscount, RefreshDiscount, home


app_name = 'main'

urlpatterns = [
    path('home/', home, name="home"),
    path('specification/add/<id>/', SpecificationAdd, name="specification_add"),
    path('room/add/<id>/', RoomAdd, name="room_add"),
    path('room/remove/<id>/', RoomRemove, name="room_remove"),
    path('room/status/<id>/', RoomChangeStatus, name="room_status"),
    path('room/ready/<id>/', RoomReady, name="room_ready"),
    path('specification/remove/<id>/', SpecificationRemove, name="sp_remove"),
    path('specification/view/<pk>/', SpecificationViewD, name="spec"),
    path('specification/change/status/<id>/', SpecificationChangeStatus, name="change_status"),
    path('specification/ready/<id>/', SpecificationReady, name="sp_ready"),
    path('specification/copy/<id>/', SpecificationCopy, name="sp_copy"),
    path('textile/review/<id>/', TextileReview, name="review_textile"),
    path('cornice/review/<id>/', CorniceReview, name="review_cornice"),

    path('textile/add/<id>/<prod_id>/', SpecificationTextileAdd, name="sp_add_textile"),
    path('cornice/add/<id>/<prod_id>/', SpecificationCorniceAdd, name="sp_add_cornice"),
    path('sewing/add/<id>/', SpecificationSewingAdd, name="sp_add_sewing"),
    path('assembly/add/<id>/', SpecificationAssemblyAdd, name="sp_add_assembly"),
    path('hanging/add/<id>/', SpecificationHangingAdd, name="sp_add_hanging"),
    path('delivery/add/<id>/', SpecificationDeliveryAdd, name="sp_add_delivery"),

    path('textile/remove/<id>/', SpecificationTextileRemove, name="sp_remove_textile"),
    path('cornice/remove/<id>/', SpecificationCorniceRemove, name="sp_remove_cornice"),
    path('sewing/remove/<id>/', SpecificationSewingRemove, name="sp_remove_sewing"),
    path('assembly/remove/<id>/', SpecificationAssemblyRemove, name="sp_remove_assembly"),
    path('hanging/remove/<id>/', SpecificationHangingRemove, name="sp_remove_hanging"),
    path('delivery/remove/<id>/', SpecificationDeliveryRemove, name="sp_remove_delivery"),

    path('orders/', OrderView, name="orders"),
    path('orders/<id>/', OrderViewD, name="order_view"),
    path('order/create/', OrderCreate, name="order_create"),
    path('order/create/<id>/', OrderCreateCustomer, name="order_cust_id"),
    path('order/remove/<id>/', OrderRemove, name="order_remove"),
    path('order/archive/<id>/', OrderArchive, name="order_archive"),

    path('test/', Test),
    path('test/<id>/', OrderCreateKp, name="order_kp"),
    path('contract/create/<id>/', ContractCreate, name="contract_create"),
    path('contract/create_xls/<id>/', ContractCreateWord, name="contract_create_xls"),
    path('contract/get/<id>/', GetContract, name="contract_get"),
    path('contract/ready/<id>/', ContractReady, name="contract_ready"),

    path('customer/create/<id>/', CustomerCreate, name="customer_create"),
    path('customer/add/', CustomerCreate, name="customer_create"),

    path('offer/create/<id>/', OfferCreate, name="offer_create"),
    path('offer/select/<id>/', OfferSelect, name="offer_select"),
    path('payment/create/<id>/', PaymentCreate, name="prepay_create"),
    path('test_template/', TestTemplate),

    path('discount/<id>/', GetDiscount, name="discount"),
    path('discount/refresh/<id>/', RefreshDiscount, name="discount_refresh"),
]
