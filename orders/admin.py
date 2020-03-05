from django.contrib import admin
from .models import Pizza,Pasta,Order_counter,User_order,Cart,Sub, DinnerPlatter, Salad

# Register your models here.
admin.site.register(Pizza)
admin.site.register(Pasta)
admin.site.register(Order_counter)
admin.site.register(User_order)
admin.site.register(Cart)
admin.site.register(Sub)
admin.site.register(DinnerPlatter)
admin.site.register(Salad)