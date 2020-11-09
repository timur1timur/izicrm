from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MarkupCustomerCategory)
admin.site.register(MarkupMaterialCategory)
admin.site.register(MarkupWorkCategory)
admin.site.register(MarkupCommon)
admin.site.register(MarkupSetting)