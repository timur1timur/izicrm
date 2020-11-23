from django.urls import path
from .views import M_OrderView, M_OrderViewD, SupplierOrderView, SupplierOrderSend, \
    M_TextileShipped, M_TextileStock, M_TextileStayOut, SupplierCornice, \
     M_CorniceShipped, M_CorniceStock, M_CorniceStayOut, \
    SupplierOrderCorniceSend, M_SewingOrder, M_AssemblyOrder, M_HangingOrder, M_DeliveryOrder, M_OrderReady, \
    M_OrderViewD_Budget, M_TextileOrderedF, M_SupplierOrders, M_TextilePayedF, SupplierOrderSend2, SupplierOrderSend3, \
    M_CorniceOrderedF, M_CornicePayedF, M_SewingPayedF, M_AssemblyPayedF, M_HangingPayedF, M_DeliveryPayedF, M_Sogl, \
    M_SoglSuccess, M_SoglDeny, M_SoglView, SupplierCorniceAddition, M_CorniceAdditionOrderedF, M_CorniceAdditionalPayedF, \
    M_CorniceAdditionalShipped, M_CorniceAdditionalStock, M_CorniceAdditionalStayOut, m_check_price, \
    m_check_price_cornice, m_check_price_additional, M_SupplierOrderedTextileEdit, M_SupplierOrderedCorniceEdit, \
    M_SupplierOrderedAdditEdit, SupplierMailList, SupplierMailView


app_name = 'manager'

urlpatterns = [
    path('orders/', M_OrderView, name="orders"),
    path('orders/<id>/', M_OrderViewD, name="order_view"),
    path('orders/budget/<id>/', M_OrderViewD_Budget, name="order_budget_view"),
    path('orders/ready/<id>/', M_OrderReady, name="order_ready"),
    path('textile/send/<id>/', SupplierOrderSend2, name="textile_send"),
    path('cornice/send/<id>/', SupplierOrderSend3, name="cornice_send"),
    path('textile/order/<id>/', SupplierOrderView, name="textile_ready"),
    path('textile/ordered/<id>/', M_TextileOrderedF, name="textile_ordered"),
    path('textile/payed/<id>/', M_TextilePayedF, name="textile_payed"),
    path('textile/shipped/<id>/', M_TextileShipped, name="textile_shipped"),
    path('textile/stock/<id>/', M_TextileStock, name="textile_stock"),
    path('textile/stayout/<id>/', M_TextileStayOut, name="textile_stay_out"),
    path('cornice/order/<id>/', SupplierCornice, name="cornice_ready"),

    path('cornice_additional/order/<id>/', SupplierCorniceAddition, name="cornice_additional_ready"),
    path('cornice_additional/ordered/<id>/', M_CorniceAdditionOrderedF, name="cornice_additional_ordered"),
    path('cornice_additional/payed/<id>/', M_CorniceAdditionalPayedF, name="cornice_additional_payed"),
    path('cornice_additional/shipped/<id>/', M_CorniceAdditionalShipped, name="cornice_additional_shipped"),
    path('cornice_additional/stock/<id>/', M_CorniceAdditionalStock, name="cornice_additional_stock"),
    path('cornice_additional/stayout/<id>/', M_CorniceAdditionalStayOut, name="cornice_additional_stay_out"),

    path('cornice/ordered/<id>/', M_CorniceOrderedF, name="cornice_ordered"),
    path('cornice/payed/<id>/', M_CornicePayedF, name="cornice_payed"),
    path('cornice/shipped/<id>/', M_CorniceShipped, name="cornice_shipped"),
    path('cornice/stock/<id>/', M_CorniceStock, name="cornice_stock"),
    path('cornice/stayout/<id>/', M_CorniceStayOut, name="cornice_stay_out"),

    path('sewing/order/<id>/', M_SewingPayedF, name="sewing_ordered"),
    path('assembly/order/<id>/', M_AssemblyPayedF, name="assembly_ordered"),
    path('hanging/order/<id>/', M_HangingPayedF, name="hanging_ordered"),
    path('delivery/order/<id>/', M_DeliveryPayedF, name="delivery_ordered"),

    path('supplier/mail/list/', SupplierMailList, name="supplier_mail_list"),
    path('supplier/mail/view/<id>/', SupplierMailView, name="supplier_mail_view"),

    path('supplier/orders/', M_SupplierOrders, name="supplier_orders"),
    path('supplier/textile_ordered/edit/<id>/', M_SupplierOrderedTextileEdit, name="supplier_ordered_textile_edit"),
    path('supplier/cornice_ordered/edit/<id>/', M_SupplierOrderedCorniceEdit, name="supplier_ordered_cornice_edit"),
    path('supplier/cornice_additional_ordered/edit/<id>/', M_SupplierOrderedAdditEdit, name="supplier_ordered_cornice_additional_edit"),

    path('sogl/list/', M_Sogl, name="sogl_list"),
    path('sogl/<id>/', M_SoglView, name="sogl_view"),
    path('sogl/<type_m>/success/<id>/', M_SoglSuccess, name="sogl_success"),
    path('sogl/<type_m>/deny/<id>/', M_SoglDeny, name="sogl_deny"),

    path('textile/ordered/<id>/check_price/<price_s>/', m_check_price, name="check_price"),
    path('cornice/ordered/<id>/check_price_cornice/<price_s>/', m_check_price_cornice, name="check_price_cornice"),
    path('cornice_additional/ordered/<id>/check_price_additional/<price_s>/', m_check_price_additional, name="check_price_additional"),

]
