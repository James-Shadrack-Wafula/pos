from django.db import models
from django.contrib.auth.models import User  # Import Django’s built-in user model

# Create your models here.
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='item_images/', null=True, blank=True)


    def __str__(self):
        return self.name

class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/')

    def __str__(self):
        return f"Image for {self.item.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to User model

    table_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def total_price(self):
        return sum(item.total_price() for item in self.order_items.all())

    def __str__(self):
        return f"Order {self.id} - Table {self.table_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def total_price(self):
        return self.quantity * self.item.unit_price

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
    

class CustomerOrder(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    table_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def total_price(self):
        return sum(item.total_price() for item in self.customer_order_items.all())

    def __str__(self):
        return f"Customer Order {self.id} - {self.user.username}"

class CustomerOrderItem(models.Model):
    customer_order = models.ForeignKey(CustomerOrder, related_name='customer_order_items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def total_price(self):
        return self.quantity * self.item.unit_price

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

class Expense(models.Model):
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"

class Added(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to User model
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    added_quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)


from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)  # For guests
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return sum(item.get_total() for item in self.cartitem_set.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.product.unit_price * self.quantity
