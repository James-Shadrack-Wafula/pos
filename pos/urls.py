from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_order/', views.create_order, name='create_order'),
    path('add_item_to_order/<int:order_id>/', views.add_item_to_order, name='add_item_to_order'),
    path('remove_item_from_order/<int:item_id>/', views.remove_item_from_order, name='remove_item_from_order'),
    path('add_item_to_stock/', views.add_item_to_stock, name='add_item_to_stock'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('summary/', views.summary, name='summary'),
]