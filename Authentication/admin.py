from django.contrib import admin
from .models import *
from Flow.models import *

admin.site.register(Event)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_validated_money_man', 'money_man_request_pending']
    actions = ['approve_money_man', 'reject_money_man']

    def approve_money_man(self, request, queryset):
        queryset.update(is_validated_money_man=True, money_man_request_pending=False)
    approve_money_man.short_description = "Approuver comme vendeur"

    def reject_money_man(self, request, queryset):
        queryset.update(money_man_request_pending=False)
    reject_money_man.short_description = "Rejeter la demande de vendeur"


admin.site.register(Utilisateur, CustomUserAdmin)