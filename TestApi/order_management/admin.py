from django.contrib import admin
from order_management.models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'updated_at')  
    list_filter = ('status', 'subtag')  

admin.site.register(Order, OrderAdmin)
