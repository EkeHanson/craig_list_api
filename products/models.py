from django.db import models
from user_registration.models import CustomUser
from django.shortcuts import reverse
# from django_countries.fields import CountryField

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

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping')
)


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name: str = 'Category'
        verbose_name_plural: str = "Categories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:category", kwargs={
            'slug': self.slug
        })


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    description_short = models.CharField(max_length=50)
    brand = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    slug = models.SlugField()
    # image_url = models.ImageField(upload_to='products/')  # Allows users to upload images
    image = models.ImageField(upload_to="media", null=True, blank=True)  # For uploaded files
    image_url = models.URLField(null=True, blank=True)  # For image URLs
    condition = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    post_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=5, decimal_places=2)  # Discount amount in percentage


class PromoCode(models.Model):
    code = models.CharField(max_length=50)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Cart {self.id}'


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

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


