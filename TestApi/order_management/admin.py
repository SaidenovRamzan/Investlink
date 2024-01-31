from django.contrib import admin
from order_management.models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'updated_at')  # Отображаемые поля в списке
    list_filter = ('status', 'subtag')  # Добавляем фильтр по статусу

admin.site.register(Order, OrderAdmin)
