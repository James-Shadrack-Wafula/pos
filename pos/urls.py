from django.urls import path
from . import views
from .views import export_excel
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('home_filter', views.home_filter, name='home_filter'),
    path('create_order/', views.create_order, name='create_order'),
    path('add_item_to_order/<int:order_id>/', views.add_item_to_order, name='add_item_to_order'),
    # path('remove_item_from_order/<int:item_id>/', views.remove_item_from_order, name='remove_item_from_order'),
    path('add_item_to_stock/', views.add_item_to_stock, name='add_item_to_stock'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('summary/', views.summary, name='summary'),
    path('export-excel/', export_excel, name='export_excel'),
    path('item-autocomplete/', views.item_autocomplete, name='item_autocomplete'),
    path('items-in-stock/', views.items_in_stock, name='items_in_stock'),
    path('increment-stock/<int:item_id>/', views.increment_stock, name='increment_stock'),
    path('update-stock/', views.update_stock_quantity, name='update_stock'),
    # path('order/<int:order_id>/item/<int:item_id>/remove/', views.remove_item_from_order, name='remove_item_from_order'),
     
    path('order/<int:order_id>/item/<int:item_id>/increment/', views.increment_item_quantity, name='increment_item_quantity'),
    path('order/<int:order_id>/item/<int:item_id>/remove/', views.remove_item_from_order, name='remove_item_from_order'),
    # path('register/', views.register, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='pos/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),

    path('order/<int:order_id>/toggle-payment/', views.toggle_payment_status, name='toggle_payment_status'),
    path('menu/', views.online_menu, name='online_menu'),
    path('customer-order/', views.place_order, name='customer-order'),


    # path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    # path("remove-from-cart/", views.remove_from_cart, name="remove_from_cart"),
    # path("get-cart-items/", views.get_cart_items, name="get_cart_items"),


    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('get-cart/', views.get_cart_data, name='get_cart'),


    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),  # API for cart count

    path("update-cart/<str:item_id>/<str:action>/", views.update_cart, name="update_cart"),

    path("clear-cart/", views.clear_cart, name="clear-cart"),
]