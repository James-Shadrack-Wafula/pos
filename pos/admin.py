from django.contrib import admin
from . models import Expense , OrderItem, Order, Item, Added
admin.site.register(Expense)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Item)
admin.site.register(Added)
# Register your models here.
