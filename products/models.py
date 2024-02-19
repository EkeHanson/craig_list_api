from django.db import models
from user_registration.models import CustomUser


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    brand = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image_url = models.ImageField(upload_to='products/')  # Allows users to upload images
    condition = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    post_date = models.DateTimeField(auto_now_add=True)
    category_choices = [
        ("Electronics", "electronics"),
        ("Fashion", "fashion"),
        ("Home & Garden", "home & garden"),
        ("Health & Beauty", "health & beauty"),
        ("Sports & Outdoors", "sports & outdoors"),
        ("Books & Music", "books & music"),
        ("Toys & Games", "toys & games"),
        ("Grocery & Gourmet Food", "grocery & gourmet food"),
        ("Automotive", "automotive"),
        ("Industrial & Scientific", "industrial & scientific"),
        ("Handmade", "handmade"),
        ("Pet Supplies", "pet supplies"),
        ("Baby", "baby"),
        ("Office Products", "office products"),
        ("Arts, Crafts & Sewing", "arts, crafts & sewing"),
        ("Movies & Television", "movies & television"),
        ("Software", "software"),
        ("Collectibles & Fine Art", "collectibles & fine art"),
        ("Musical Instruments", "musical instruments")
    ]
    category = models.CharField(max_length=35, choices=category_choices)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f'Cart {self.id}'


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'Cart Item {self.id}'


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.TextField()
    order_status_choice = (
            ('P', 'Pending'),
            ('PR', 'Processing'),
            ('S', 'Shipped'),
            ('D', 'Delivered'),
            ('C', 'Cancelled')
        )
    order_status = models.CharField(max_length=2, choices=order_status_choice)

    def __str__(self):
        return f'Order {self.id}'


# class Order(models.Model):
#     user = models.CharField(max_length=255)
#     products = models.JSONField()
#     quantity = models.PositiveIntegerField()
#     total_price = models.FloatField()
#     order_status_choice = (
#         ('P', 'Pending'),
#         ('PR', 'Processing'),
#         ('S', 'Shipped'),
#         ('D', 'Delivered'),
#         ('C', 'Cancelled')
#     )
#     order_status = models.CharField(max_length=2, choices=order_status_choice)


