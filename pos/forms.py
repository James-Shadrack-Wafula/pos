from django import forms
from .models import Item, Order, OrderItem, Expense

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'unit_price', 'stock_quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount']