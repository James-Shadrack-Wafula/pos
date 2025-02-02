from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Order, OrderItem, Expense
from .forms import ItemForm, OrderForm, OrderItemForm, ExpenseForm

# 
from django.shortcuts import render
from django.utils.dateparse import parse_date
from .models import Order

def home(request):
    orders = Order.objects.filter(is_paid=False)

    return render(request, 'pos/home.html', {'orders': orders})


def home_filter(request):
    orders = Order.objects.filter(is_paid=False)
    start_date = request.GET.get('start_date')
    end_date  = request.GET.get('end_date')

    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        if start_date and end_date:
            orders = orders.filter(created_at__date__range=[start_date, end_date])
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

from django.shortcuts import render
from django.utils.dateparse import parse_date
from .models import Order, Item, Expense

def summary(request):
    items = Item.objects.all()
    orders = Order.objects.all()  # Fetch all orders
    expenses = Expense.objects.all()  # Fetch all expenses

    # Get start and end date from the request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        
        if start_date and end_date:
            orders = orders.filter(created_at__date__range=[start_date, end_date])
            expenses = expenses.filter(date__range=[start_date, end_date])  # Assuming `date` is the field for Expense

    # Calculate total values
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
        'orders': orders  # Pass filtered orders
    })



import pandas as pd
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from .models import Item, Order


import pandas as pd
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from .models import Item, OrderItem, Order

def export_excel(request):
    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    page = request.GET.get('page', 'home')  # Default to home

    # Fetch orders based on page selection
    orders = Order.objects.all()
    if page == "home":
        orders = orders.filter(is_paid=False)

    # Filter orders based on date
    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        if start_date and end_date:
            orders = orders.filter(created_at__date__range=[start_date, end_date])

    # Fetch order items linked to filtered orders
    order_items = OrderItem.objects.filter(order__in=orders)

    # Prepare Data for Excel
    data = []
    items = Item.objects.all()  # Fetch all items

    for item in items:
        opening = item.stock_quantity  # Initial stock
        added = sum(oi.quantity for oi in order_items if oi.item == item)  # Stock added from orders
        stock_total = opening + added
        sells = sum(oi.quantity for oi in order_items if oi.item == item)  # Sold items
        closing = stock_total - sells
        unit_price = item.unit_price
        cash_sells = sells * unit_price

        data.append([
            item.name, opening, added, stock_total, sells, closing, unit_price, cash_sells
        ])

    # Create DataFrame
    df = pd.DataFrame(data, columns=["Item Name", "Opening", "Added", "Stock Total", "Sells", "Closing", "Unit Price", "Cash Sells"])

    # Add Total Row
    total_cash_sales = df["Cash Sells"].sum()
    df.loc["Total"] = ["", "", "", "", "", "", "Total Sales", total_cash_sales]

    file_name = f"filtered_data_{start_date}_{end_date}.xlsx"
    # Convert to Excel
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    df.to_excel(response, index=False)

    return response


# def export_excel(request):
#     # Get filter parameters
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     page = request.GET.get('page', 'home')  # Default to home

#     # Fetch items
#     items = Item.objects.all()

#     # Fetch orders based on page selection
#     if page == "home":
#         orders = Order.objects.filter(is_paid=False)
#     else:
#         orders = Order.objects.all()

#     # Filter orders based on date
#     if start_date and end_date:
#         start_date = parse_date(start_date)
#         end_date = parse_date(end_date)
#         if start_date and end_date:
#             orders = orders.filter(created_at__date__range=[start_date, end_date])

#     # Prepare Data for Excel
#     data = []
#     for item in items:
#         opening = item.stock_quantity  # Initial stock
#         added = sum(order.quantity for order in orders if order.item == item)  # Added stock
#         stock_total = opening + added
#         sells = sum(order.quantity_sold for order in orders if order.item == item)  # Sold items
#         closing = stock_total - sells
#         unit_price = item.unit_price
#         cash_sells = sells * unit_price

#         data.append([
#             item.name, opening, added, stock_total, sells, closing, unit_price, cash_sells
#         ])

#     # Create DataFrame
#     df = pd.DataFrame(data, columns=["Item Name", "Opening", "Added", "Stock Total", "Sells", "Closing", "Unit Price", "Cash Sells"])

#     # Add Total Row
#     total_cash_sales = df["Cash Sells"].sum()
#     df.loc["Total"] = ["", "", "", "", "", "", "Total Sales", total_cash_sales]

#     # Convert to Excel
#     response = HttpResponse(content_type='application/vnd.ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="filtered_data.xlsx"'
#     df.to_excel(response, index=False)

#     return response



# def summary(request):
#     items = Item.objects.all()
#     orders = Order.objects.all()  # Only count paid orders
#     # orders = Order.objects.filter(is_paid=True)  # Only count paid orders
#     expenses = Expense.objects.all()

#     total_stock_value = sum(item.unit_price * item.stock_quantity for item in items)
#     total_expenses = sum(expense.amount for expense in expenses)
#     total_sales = sum(order.total_price() for order in orders)

#     # Preparing data for charts
#     stock_labels = [item.name for item in items]
#     stock_values = [item.stock_quantity for item in items]

#     expense_labels = [expense.description for expense in expenses]
#     expense_values = [expense.amount for expense in expenses]

#     return render(request, 'pos/summary.html', {
#         'total_stock_value': total_stock_value,
#         'total_expenses': total_expenses,
#         'total_sales': total_sales,
#         'stock_labels': stock_labels,
#         'stock_values': stock_values,
#         'expense_labels': expense_labels,
#         'expense_values': expense_values,
#         'orders': orders
#     })

# def summary(request):
#     items = Item.objects.all()
#     total_stock_value = sum(item.unit_price * item.stock_quantity for item in items)
#     expenses = Expense.objects.all()
#     total_expenses = sum(expense.amount for expense in expenses)
#     return render(request, 'pos/summary.html', {
#         'total_stock_value': total_stock_value,
#         'total_expenses': total_expenses
#     })