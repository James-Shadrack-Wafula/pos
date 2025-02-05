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
    # item = Item.objects.get(id=)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order

            # Get the item from the form
            item = order_item.item

            # Check if the item is in stock
            if item.stock_quantity > 0:
                # Save the order item
                order_item.save()

                # Reduce the item's stock quantity by 1
                item.stock_quantity -= order_item.quantity
                item.save()

            # order_item.save()
            return redirect('home')
    else:
        form = OrderItemForm()
    return render(request, 'pos/add_item_to_order.html', {'form': form, 'order': order})

# def remove_item_from_order(request, item_id):
#     item = get_object_or_404(OrderItem, id=item_id)
#     item.delete()
#     return redirect('home')

from django.shortcuts import get_object_or_404, redirect
from .models import Order, OrderItem
# THis is in the order Card
def increment_item_quantity(request, order_id, item_id):
    order = get_object_or_404(Order, id=order_id)
    item = get_object_or_404(OrderItem, id=item_id, order=order)

    # Increment the quantity and save the changes
    item.quantity += 1
    item.total_price = item.item.unit_price * item.quantity
    item.save()

    # Redirect to the same order page
    return redirect('home')


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Order, OrderItem

def remove_item_from_order(request, order_id, item_id):
    order = get_object_or_404(Order, id=order_id)
    item = get_object_or_404(OrderItem, id=item_id, order=order)
    
    # Remove item from order
    item.delete()

    messages.success(request, 'Item removed successfully.')
    return redirect('home', order_id=order.id)  # Adjust URL as needed


def add_item_to_stock(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ItemForm()
    return render(request, 'pos/add_item_to_stock.html', {'form': form})

from django.http import JsonResponse
def item_autocomplete(request):
    if 'term' in request.GET:
        qs = Item.objects.filter(name__icontains=request.GET.get('term'))
        names = list(qs.values_list('name', flat=True))
        return JsonResponse(names, safe=False)
# def item_autocomplete(request):
#     if 'term' in request.GET:
#         qs = Item.objects.filter(name__icontains=request.GET.get('term'))
#         names = list(qs.values_list('name', flat=True))
#         return JsonResponse(names, safe=False)



# TRY VERSION 2

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Item

def items_in_stock(request):
    """Display all items in stock with their stock quantity."""
    items = Item.objects.all()
    return render(request, 'pos/items_in_stock.html', {'items': items})

def increment_stock(request, item_id):
    """Increment stock quantity for a given item."""
    item = get_object_or_404(Item, id=item_id)
    item.stock_quantity += 1
    item.save()
    return JsonResponse({'success': True, 'new_quantity': item.stock_quantity})


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Item

def items_in_stock(request):
    items = Item.objects.all()
    return render(request, 'pos/items_in_stock.html', {'items': items})

from django.contrib import messages
def update_stock_quantity(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        additional_quantity = request.POST.get("additional_quantity")

        try:
            item = get_object_or_404(Item, id=item_id)
            additional_quantity = int(additional_quantity)

            if additional_quantity > 0:
                item.stock_quantity += additional_quantity
                item.save()
                messages.success(request, f"Stock for {item.name} updated successfully by {additional_quantity} units.")
                return redirect("items_in_stock")  # Redirect back to the items list

        except ValueError:
            messages.error(request, "Please enter a valid quantity.")
        
    return redirect("items_in_stock")  # Redirect back in case of failure
    # if request.method == "POST":
    #     item_id = request.POST.get("item_id")
    #     additional_quantity = request.POST.get("additional_quantity")

    #     try:
    #         item = get_object_or_404(Item, id=item_id)
    #         additional_quantity = int(additional_quantity)

    #         if additional_quantity > 0:
    #             item.stock_quantity += additional_quantity
    #             item.save()
    #             return redirect("items_in_stock")  # Redirect back to the items list

    #     except ValueError:
    #         return JsonResponse({"success": False, "error": "Invalid quantity."})

    # return JsonResponse({"success": False, "error": "Invalid request."})
    # if request.method == "POST":
    #     item_id = request.POST.get("item_id")
    #     additional_quantity = request.POST.get("additional_quantity")

    #     try:
    #         item = Item.objects.get(id=item_id)
    #         additional_quantity = int(additional_quantity)

    #         if additional_quantity > 0:
    #             item.stock_quantity += additional_quantity
    #             item.save()
    #             return JsonResponse({"success": True, "new_quantity": item.stock_quantity})

    #     except (Item.DoesNotExist, ValueError, TypeError):
    #         return JsonResponse({"success": False, "error": "Invalid request."})

    # return JsonResponse({"success": False, "error": "Invalid method."})



    # if request.method == "POST":
    #     item_id = request.POST.get('item_id')
    #     additional_quantity = int(request.POST.get('additional_quantity', 0))

    #     if item_id and additional_quantity > 0:
    #         item = Item.objects.get(id=item_id)
    #         item.stock_quantity += additional_quantity
    #         item.save()
    #         return JsonResponse({"success": True, "new_quantity": item.stock_quantity})

    # return JsonResponse({"success": False, "error": "Invalid request"})

# CLOSING TRY VERSION 2


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
        'orders': orders,  # Pass filtered orders
        'expenses': expenses
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
        # added = sum(oi.quantity for oi in order_items if oi.item == item)  # Stock added from orders
        # stock_total = opening + added
        sells = sum(oi.quantity for oi in order_items if oi.item == item)  # Sold items
        closing = opening - sells
        unit_price = item.unit_price
        cash_sells = sells * unit_price

        data.append([
            item.name, opening, sells, closing, unit_price, cash_sells
        ])

    # Create DataFrame
    # df = pd.DataFrame(data, columns=["Item Name", "Opening", "Added", "Stock Total", "Sells", "Closing", "Unit Price", "Cash Sells"])
    df = pd.DataFrame(data, columns=["Item Name", "Opening", "Sells", "Closing", "Unit Price", "Cash Sells"])

    # Add Total Row
    total_cash_sales = df["Cash Sells"].sum()
    df.loc["Total"] = ["", "", "", "", "Total Sales", total_cash_sales]

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