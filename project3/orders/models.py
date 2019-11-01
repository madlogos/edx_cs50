from django.db import models
from django.contrib.auth.models import User

# Create your models here.
SIZE_CHOICES = (
    ('Small', 'Small'),
    ('Large', 'Large'),
    ('Regular', 'Regular')
)
ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Paid', 'Paid'),
    ('Completed', 'Completed'),
    ('Failed', 'Failed'),
    ('Cancelled', 'Cancelled'),
)

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        db_table = "shop_category"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=128)
    size = models.CharField(max_length=8, choices=SIZE_CHOICES, default='Regular')
    n_topping = models.IntegerField(default=0)
    n_addition = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        db_table = "shop_product"
        unique_together = (('category', 'name', 'size'), )

    def __str__(self):
        return f"{self.category} - {self.name} ({self.size})"


class Topping(models.Model):
    name = models.CharField(max_length=128, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "topping"
        verbose_name_plural = "toppings"
        db_table = "shop_topping"

    def __str__(self):
        return self.name


class Addition(models.Model):
    name = models.CharField(max_length=128)
    size = models.CharField(max_length=8, choices=SIZE_CHOICES, default='Regular')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "addition"
        verbose_name_plural = "additions"
        db_table = "shop_addition"
        unique_together = (('name', 'size'), )

    def __str__(self):
        return f"{self.name} ({self.size})"


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products")
    quantity = models.IntegerField(default=0)
    topping = models.ManyToManyField(Topping, related_name="toppings", through="ItemTopping")
    addition = models.ManyToManyField(Addition, related_name="additions", through="ItemAddition")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "item"
        verbose_name_plural = "items"

    def __str__(self):
        return f"{self.product} x {self.quantity}"


class ItemTopping(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="itemtopping_item")
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE, related_name="itemtopping_topping")
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name = "item_topping"
        verbose_name_plural = "item_toppings"

    def __str__(self):
        return f"{self.item} - {self.topping} x {self.quantity}"


class ItemAddition(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="itemaddition_item")
    addition = models.ForeignKey(Addition, on_delete=models.CASCADE, related_name="itemaddition_addition")
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name = "item_addition"
        verbose_name_plural = "item_additions"

    def __str__(self):
        return f"{self.item} - {self.addition} x {self.quantity}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_users")
    item = models.ManyToManyField(Item, related_name="cart_items", through="CartItem")

    class Meta:
        verbose_name = "cart"
        verbose_name_plural = "carts"

    def __str__(self):
        return f"{self.user}\'s cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name = "cart_item"
        verbose_name_plural = "cart_items"

    def __str__(self):
        return f"{self.cart} - {self.item} x {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="order_users")
    item = models.ManyToManyField(Item, related_name="order_items", through="OrderItem")
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=8, choices=ORDER_STATUS, default='Pending')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name = "order_item"
        verbose_name_plural = "order_items"

    def __str__(self):
        return f"{self.order} - {self.item} x {self.quantity}"