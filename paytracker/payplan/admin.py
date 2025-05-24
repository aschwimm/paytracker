from django.contrib import admin
from .models import Payplan, Sale, VolumeBonus, Flat
# Register your models here.

class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "profit", "salecredit", "datelogged")

admin.site.register(Payplan),
admin.site.register(Sale, SaleAdmin)
admin.site.register(VolumeBonus),
admin.site.register(Flat)