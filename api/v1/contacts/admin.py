from django.contrib import admin

from .models import AreaCode, Contact, Telecom

# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'name', 'area_code', 'number', 'email', 'address']

@admin.register(AreaCode)
class AreaCodeAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'code']

@admin.register(Telecom)
class TelecomAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'name']