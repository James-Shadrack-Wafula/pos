from django.contrib import admin
from . models import Expense , OrderItem, Order, Item
admin.site.register(Expense)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Item)

# Register your models here.
