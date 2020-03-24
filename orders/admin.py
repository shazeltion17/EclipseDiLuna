from django.contrib import admin
from .models import menu_items,Order_counter,User_order,Cart

# Register your models here.
admin.site.register(menu_items)
admin.site.register(Order_counter)
admin.site.register(User_order)
admin.site.register(Cart)