from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Order, OrderItem, Expense
from .forms import ItemForm, OrderForm, OrderItemForm, ExpenseForm

def home(request):
    orders = Order.objects.filter(is_paid=False)
    return render(request, 'pos/home.html', {'orders': orders})

from django.shortcuts import render

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = OrderForm()
    return render(request, 'pos/create_order.html', {'form': form})
# def create_order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = OrderForm()
#     return render(request, 'pos/create_order.html', {'form': form})

def add_item_to_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()
            return redirect('home')
    else:
        form = OrderItemForm()
    return render(request, 'pos/add_item_to_order.html', {'form': form, 'order': order})

def remove_item_from_order(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    item.delete()
    return redirect('home')

def add_item_to_stock(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ItemForm()
    return render(request, 'pos/add_item_to_stock.html', {'form': form})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'pos/add_expense.html', {'form': form})


from django.shortcuts import render
from .models import Item, Expense, Order

def summary(request):
    items = Item.objects.all()
    orders = Order.objects.all()  # Only count paid orders
    # orders = Order.objects.filter(is_paid=True)  # Only count paid orders
    expenses = Expense.objects.all()

    total_stock_value = sum(item.unit_price * item.stock_quantity for item in items)
    total_expenses = sum(expense.amount for expense in expenses)
    total_sales = sum(order.total_price() for order in orders)

    # Preparing data for charts
    stock_labels = [item.name for item in items]
    stock_values = [item.stock_quantity for item in items]

    expense_labels = [expense.description for expense in expenses]
    expense_values = [expense.amount for expense in expenses]

    return render(request, 'pos/summary.html', {
        'total_stock_value': total_stock_value,
        'total_expenses': total_expenses,
        'total_sales': total_sales,
        'stock_labels': stock_labels,
        'stock_values': stock_values,
        'expense_labels': expense_labels,
        'expense_values': expense_values,
        'orders': orders
    })

# def summary(request):
#     items = Item.objects.all()
#     total_stock_value = sum(item.unit_price * item.stock_quantity for item in items)
#     expenses = Expense.objects.all()
#     total_expenses = sum(expense.amount for expense in expenses)
#     return render(request, 'pos/summary.html', {
#         'total_stock_value': total_stock_value,
#         'total_expenses': total_expenses
#     })