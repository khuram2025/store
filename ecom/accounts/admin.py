from django.contrib import admin
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_number',)  # customize the fields to display
    search_fields = ('name', 'mobile_number',)  # add a search box to search these fields

admin.site.register(Account, AccountAdmin)
