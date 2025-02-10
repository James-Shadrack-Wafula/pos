from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Order, OrderItem, Expense
from .forms import ItemForm, OrderForm, OrderItemForm, ExpenseForm

# 
from django.shortcuts import render
from django.utils.dateparse import parse_date
from .models import Order


from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()
            login(request, user)
            return redirect('home')  # Redirect to homepage or dashboard
    else:
        form = RegisterForm()
    return render(request, 'pos/register.html', {'form': form})


from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def custom_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")  # Redirect to your homepage or dashboard
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "login.html")  # Load the login template




from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home(request):
    orders = Order.objects.filter(is_paid=False)

    return render(request, 'pos/home.html', {'orders': orders})

@login_required
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


@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)  # Do not save yet
            order.user = request.user  # Assign logged-in user
            order.save()  # Now save the order
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
# def create_order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = OrderForm()
#     return render(request, 'pos/create_order.html', {'form': form})

@login_required
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

@login_required
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

@login_required
def remove_item_from_order(request, order_id, item_id):
    order = get_object_or_404(Order, id=order_id)
    item = get_object_or_404(OrderItem, id=item_id, order=order)
    
    # Remove item from order
    item.delete()

    messages.success(request, 'Item removed successfully.')
    return redirect('home', order_id=order.id)  # Adjust URL as needed

@login_required
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
from .models import Item, Added

def items_in_stock(request):
    items = Item.objects.all()
    return render(request, 'pos/items_in_stock.html', {'items': items})

from django.contrib import messages
@login_required
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
                # Create an Added object to track stock update
                Added.objects.create(
                    user=request.user,  # Capture the logged-in user
                    item=item,
                    added_quantity=additional_quantity
                )

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


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order

@login_required
def toggle_payment_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Toggle the `is_paid` field
    order.is_paid = not order.is_paid
    order.save()
    
    status = "Paid" if order.is_paid else "Unpaid"
    messages.success(request, f"Order for Table {order.table_number} marked as {status}.")
    
    return redirect(request.META.get("HTTP_REFERER", "orders_page"))  # Redirect back to orders page


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

from django.http import HttpResponse
import pandas as pd
from django.utils.dateparse import parse_date
from django.db.models import Sum
from .models import Item, Order, OrderItem, Added


from django.http import HttpResponse
import pandas as pd
from django.utils.dateparse import parse_date
from django.db.models import Sum
from .models import Item, OrderItem, Added

def export_excel(request):
    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
    else:
        return HttpResponse("Invalid date range", status=400)

    # Fetch all items
    items = Item.objects.all()

    # Prepare Data for Excel
    data = []

    for item in items:
        # Start with the current stock quantity
        current_stock = item.stock_quantity  

        # **Determine Stock at End Date**
        # Add back items sold *AFTER* the end date
        items_sold_after = OrderItem.objects.filter(
            item=item, order__created_at__date__gt=end_date
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0

        # Subtract items added *AFTER* the end date
        items_added_after = Added.objects.filter(
            item=item, date__gt=end_date
        ).aggregate(Sum('added_quantity'))['added_quantity__sum'] or 0

        stock_on_end_date = current_stock + items_sold_after - items_added_after

        # **Find Items Added During the Period**
        added = Added.objects.filter(
            item=item, date__range=[start_date, end_date]
        ).aggregate(Sum('added_quantity'))['added_quantity__sum'] or 0

        # **Find Items Sold During the Period**
        sells = OrderItem.objects.filter(
            item=item, order__created_at__date__range=[start_date, end_date]
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0

        # **Calculate Opening Stock**
        opening = stock_on_end_date - added + sells

        # **Calculate Closing Stock**
        closing = opening + added - sells

        # **Calculate Cash Sales**
        unit_price = item.unit_price
        cash_sells = sells * unit_price

        data.append([
            item.name, opening, added, sells, closing, unit_price, cash_sells
        ])

    # Create DataFrame
    df = pd.DataFrame(data, columns=["Item Name", "Opening", "Added", "Sells", "Closing", "Unit Price", "Cash Sells"])

    # Add Total Row
    total_cash_sales = df["Cash Sells"].sum()
    df.loc["Total"] = ["", "", "", "", "", "Total Sales", total_cash_sales]

    file_name = f"filtered_data_{start_date}_{end_date}.xlsx"

    # Convert to Excel
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    df.to_excel(response, index=False)

    return response


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Item, CustomerOrder, CustomerOrderItem

# View for displaying the menu
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Item, CustomerOrder, CustomerOrderItem

# View for displaying the menu
def online_menu(request):
    items = Item.objects.all()
    """Render the online menu with the cart count."""
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())  # Count total items

    return render(request, 'pos/online_menu.html', {'items': items, 'cart_count': cart_count})

# View for handling the checkout process

import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem


import json
from django.http import JsonResponse
from .models import Order, OrderItem, Item  # Ensure these models are correctly imported
@csrf_exempt
def place_order(request):
    if request.method == "POST":
        try:
            print("Raw Request Body:", request.body)  # Debugging Output

            # Get form data
            table_number = request.POST.get("table_number")
            cart_data = request.POST.get("cart")  # JSON string

            if not table_number or not cart_data:
                return JsonResponse({"error": "Missing table number or cart data"}, status=400)

            cart = json.loads(cart_data)  # Convert JSON string to Python list

            # Create the order
            order = Order.objects.create(table_number=table_number)

            # Iterate over cart items and create OrderItem instances
            for item in cart:
                item_name = item.get("name")  # Get item name from JSON
                quantity = item.get("quantity")
                
                # Validate required fields
                if not item_name or quantity is None:
                    return JsonResponse({"error": "Invalid item data"}, status=400)

                # Fetch the Item instance from the database
                try:
                    item_instance = Item.objects.get(name=item_name)
                except Item.DoesNotExist:
                    return JsonResponse({"error": f"Item '{item_name}' does not exist"}, status=400)

                # Create OrderItem with the correct Item instance
                OrderItem.objects.create(
                    order=order,
                    item=item_instance,  # ✅ Correcting this line
                    # price=item_instance.unit_price,  # Ensure price is fetched from DB
                    quantity=quantity
                )

            messages.success(request, "Order placed successfully!")
            return redirect("online_menu")  # ✅ Redirect to the online menu

        except Exception as e:
            print("Exception:", str(e))  # Debugging Output
            messages.error(request, "An error occurred while placing the order.")
            return redirect("online_menu")

    messages.error(request, "Invalid request method")
    return redirect("online_menu")
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from .models import Cart, CartItem, Item

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Item

def add_to_cart(request, item_id):
    """Add an item to the cart stored in the session."""
    cart = request.session.get('cart', {})
    item = Item.objects.get(id=item_id)
    
    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] += 1
    else:
        item = Item.objects.get(id=item_id)
        cart[str(item_id)] = {
            'name': item.name,
            'price': float(item.unit_price),
            'quantity': 1
        }

    request.session['cart'] = cart  # Save cart in session

     # ✅ Add a success message
    messages.success(request, f"{item.name} has been added to your cart!")

    return redirect('online_menu')  # Redirect back to menu page

def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        del cart[str(item_id)]
        request.session['cart'] = cart

    return redirect('menu')

def get_cart_data(request):
    """Fetch the cart data to update the modal dynamically."""
    cart = request.session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    return JsonResponse({'cart': cart, 'total_price': total_price})



from django.http import JsonResponse

def get_cart_count(request):
    """Returns the cart count as JSON for AJAX updates."""
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())  # Calculate count
    return JsonResponse({'count': cart_count})





from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Item  # Import Item model

def update_cart(request, item_id, action):
    """Handles cart updates for increasing, decreasing, or removing items."""
    cart = request.session.get('cart', {})

    if item_id not in cart:
        return JsonResponse({"error": "Item not in cart"}, status=400)

    if action == "increase":
        cart[item_id]["quantity"] += 1
    elif action == "decrease":
        cart[item_id]["quantity"] = max(1, cart[item_id]["quantity"] - 1)
    elif action == "remove":
        del cart[item_id]

    request.session["cart"] = cart  # Save updated cart
    cart_count = sum(item["quantity"] for item in cart.values())

    return JsonResponse({"cart": cart, "cart_count": cart_count})


from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.contrib import messages

def clear_cart(request):
    """Clear the shopping cart from the session and redirect to the menu with a success message."""
    if request.method == "POST":
        request.session['cart'] = {}  # Clear the cart
        request.session.modified = True
        messages.success(request, "Cart has been cleared successfully.")  # Display message
        return render(request, "pos/online_menu.html", {"message": "Cart cleared successfully!"})  # Render menu page

    return render(request, "pos/online_menu.html", {"message": "An error occured"})  # Render menu page

    # return JsonResponse({"error": "Invalid request"}, status=400)


# def clear_cart(request):
#     """Clear the shopping cart from the session and show a success message."""
#     if request.method == "POST":
#         request.session['cart'] = {}  # Clear the cart
#         request.session.modified = True
#         messages.success(request, "Cart has been cleared successfully.")  # Add success message
#     return redirect("online_menu")
    # return render(request, "pos/online_menu.html")  # Render online_menu.html with the message

# def clear_cart(request):
#     """Clear the shopping cart from the session."""
#     if request.method == "POST":
#         request.session['cart'] = {}
#         request.session.modified = True
#         return JsonResponse({"success": True})
#     return JsonResponse({"error": "Invalid request"}, status=400)

# def get_cart(request):
#     """Retrieve the user's cart or create a new one if none exists."""
#     if request.user.is_authenticated:
#         cart, created = Cart.objects.get_or_create(user=request.user)
#     else:
#         session_id = request.session.session_key
#         if not session_id:
#             request.session.create()
#             session_id = request.session.session_key
#         cart, created = Cart.objects.get_or_create(session_id=session_id)
#     return cart

# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from .models import Item

# def add_to_cart(request, item_id):
#     """Add an item to the cart stored in the session."""
#     cart = request.session.get('cart', {})

#     if item_id in cart:
#         cart[item_id]['quantity'] += 1
#     else:
#         item = Item.objects.get(id=item_id)
#         cart[item_id] = {'name': item.name, 'price': item.unit_price, 'quantity': 1}

#     request.session['cart'] = cart  # Save cart in session
#     return redirect('menu')  # Redirect back to menu page

# def remove_from_cart(request, item_id):
#     """Remove an item from the cart."""
#     cart = request.session.get('cart', {})

#     if item_id in cart:
#         del cart[item_id]
#         request.session['cart'] = cart

#     return redirect('menu')

# def view_cart(request):
#     """Display the cart."""
#     cart = request.session.get('cart', {})
#     total_price = sum(item['price'] * item['quantity'] for item in cart.values())

#     return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})


# def get_cart_items(request):
#     """Retrieve cart items for display."""
#     cart = get_cart(request)
#     items = [
#         {"id": item.product.id, "name": item.product.name, "quantity": item.quantity, "price": item.product.unit_price}
#         for item in cart.cartitem_set.all()
#     ]
#     return JsonResponse({"cart": items, "total": cart.get_total_price()})

# @csrf_exempt  # Remove this if CSRF is handled via the form
# def place_order(request):
#     if request.method == "POST":
#         try:
#             table_number = request.POST.get("table_number")
#             cart_data = request.POST.get("cart")  # This will be a JSON string

#             if not table_number or not cart_data:
#                 return JsonResponse({"error": "Missing table number or cart data"}, status=400)

#             cart = json.loads(cart_data)  # Convert JSON string to Python list

#             # Save the order in the database
#             order = Order.objects.create(table_number=table_number, status="Pending")

#             # Save order items
#             for item in cart:
#                 OrderItem.objects.create(
#                     order=order,
#                     item_name=item["name"],
#                     price=item["price"],
#                     quantity=item["quantity"]
#                 )

#             return JsonResponse({"message": "Order placed successfully", "order_id": order.id}, status=200)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Invalid request method"}, status=400)

# def place_order(request, table_number):
#     if request.method == "POST":
#         cart = request.POST.get('cart', '[]')
#         cart_items = eval(cart)  # Convert string to list
#         if not cart_items:
#             return JsonResponse({'error': 'Cart is empty'}, status=400)

#         order = CustomerOrder.objects.create(table_number=table_number, is_paid=False)
#         for item in cart_items:
#             item_obj = Item.objects.get(id=item['id'])
#             CustomerOrderItem.objects.create(
#                 customer_order=order,
#                 item=item_obj,
#                 quantity=item['quantity']
#             )
#         return JsonResponse({'message': 'Order placed successfully!', 'order_id': order.id})

#     return JsonResponse({'error': 'Invalid request'}, status=400)


# def export_excel(request):
#     # Get filter parameters
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     page = request.GET.get('page', 'home')  # Default to home

#     # Fetch orders based on page selection
#     orders = Order.objects.all()
#     if page == "home":
#         orders = orders.filter(is_paid=False)

#     # Filter orders based on date
#     if start_date and end_date:
#         start_date = parse_date(start_date)
#         end_date = parse_date(end_date)
#         if start_date and end_date:
#             orders = orders.filter(created_at__date__range=[start_date, end_date])

#     # Fetch order items linked to filtered orders
#     order_items = OrderItem.objects.filter(order__in=orders)

#     # Prepare Data for Excel
#     data = []
#     items = Item.objects.all()  # Fetch all items

#     for item in items:
#         # **Calculate Opening Stock**
#         # Stock before the filter period (sum of all added - sum of all sold before the start date)
#         added_before = Added.objects.filter(item=item, date__lt=start_date).aggregate(Sum('added_quantity'))['added_quantity__sum'] or 0
#         sold_before = OrderItem.objects.filter(item=item, order__created_at__date__lt=start_date).aggregate(Sum('quantity'))['quantity__sum'] or 0
#         opening = added_before - sold_before

#         # **Stock Added During the Period**
#         added = Added.objects.filter(item=item, date__range=[start_date, end_date]).aggregate(Sum('added_quantity'))['added_quantity__sum'] or 0

#         # **Stock Sold During the Period**
#         sells = order_items.filter(item=item).aggregate(Sum('quantity'))['quantity__sum'] or 0

#         # **Calculate Closing Stock**
#         closing = (opening + added) - sells

#         unit_price = item.unit_price
#         cash_sells = sells * unit_price

#         data.append([
#             item.name, opening, added, sells, closing, unit_price, cash_sells
#         ])

#     # Create DataFrame
#     df = pd.DataFrame(data, columns=["Item Name", "Opening", "Added", "Sells", "Closing", "Unit Price", "Cash Sells"])

#     # Add Total Row
#     total_cash_sales = df["Cash Sells"].sum()
#     df.loc["Total"] = ["", "", "", "", "", "Total Sales", total_cash_sales]

#     file_name = f"filtered_data_{start_date}_{end_date}.xlsx"
    
#     # Convert to Excel
#     response = HttpResponse(content_type='application/vnd.ms-excel')
#     response['Content-Disposition'] = f'attachment; filename="{file_name}"'
#     df.to_excel(response, index=False)

#     return response


# def export_excel(request):
#     # Get filter parameters
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     page = request.GET.get('page', 'home')  # Default to home

#     # Fetch orders based on page selection
#     orders = Order.objects.all()
#     if page == "home":
#         orders = orders.filter(is_paid=False)

#     # Filter orders based on date
#     if start_date and end_date:
#         start_date = parse_date(start_date)
#         end_date = parse_date(end_date)
#         if start_date and end_date:
#             orders = orders.filter(created_at__date__range=[start_date, end_date])

#     # Fetch order items linked to filtered orders
#     order_items = OrderItem.objects.filter(order__in=orders)

#     # Prepare Data for Excel
#     data = []
#     items = Item.objects.all()  # Fetch all items

#     for item in items:
#         opening = item.stock_quantity  # Initial stock
#         # added = sum(oi.quantity for oi in order_items if oi.item == item)  # Stock added from orders
#         # stock_total = opening + added
#         sells = sum(oi.quantity for oi in order_items if oi.item == item)  # Sold items
#         closing = opening - sells
#         unit_price = item.unit_price
#         cash_sells = sells * unit_price

#         data.append([
#             item.name, opening, sells, closing, unit_price, cash_sells
#         ])

#     # Create DataFrame
#     # df = pd.DataFrame(data, columns=["Item Name", "Opening", "Added", "Stock Total", "Sells", "Closing", "Unit Price", "Cash Sells"])
#     df = pd.DataFrame(data, columns=["Item Name", "Opening", "Sells", "Closing", "Unit Price", "Cash Sells"])

#     # Add Total Row
#     total_cash_sales = df["Cash Sells"].sum()
#     df.loc["Total"] = ["", "", "", "", "Total Sales", total_cash_sales]

#     file_name = f"filtered_data_{start_date}_{end_date}.xlsx"
#     # Convert to Excel
#     response = HttpResponse(content_type='application/vnd.ms-excel')
#     response['Content-Disposition'] = f'attachment; filename="{file_name}"'
#     df.to_excel(response, index=False)

#     return response


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