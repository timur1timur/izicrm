from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Contract)
admin.site.register(Specification)
admin.site.register(OrderItemTextile1)
admin.site.register(OrderItemCornice)
admin.site.register(OrderItemWorkSewing)
admin.site.register(OrderItemWorkAssembly)
admin.site.register(OrderItemWorkHanging)
admin.site.register(OrderItemWorkDelivery)
admin.site.register(Order)
admin.site.register(Room)
admin.site.register(OfferVersion)
admin.site.register(Offer)
admin.site.register(OrderDoc)
admin.site.register(Payment)
admin.site.register(PaymentCategory)
admin.site.register(SupplierOrder)
admin.site.register(SupplierOrderCornice)
admin.site.register(OrderItemCorniceAdditional)



