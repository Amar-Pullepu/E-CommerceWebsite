from django.contrib import admin

# Register your models here.
from .models import Item, OrderItem, Order, Price, Category, SubCategory

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Price)
admin.site.register(Category)
admin.site.register(SubCategory)