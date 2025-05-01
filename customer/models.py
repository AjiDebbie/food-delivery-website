from django.conf import settings
from django.db import models
from django.contrib.auth.models import User






# Create your models here.


class Item(models.Model):
    CATEGORY_CHOICES = (
    ("DRINKS","Drinks"),
    ("DESSERTS","Desserts"),
    ("BURGER","Burger"),
    ("PIZZA","Pizza"),
)
    RATING=(
    ('⭐','⭐'),
    ('⭐⭐','⭐⭐'),
    ('⭐⭐⭐','⭐⭐⭐'),
    ('⭐⭐⭐⭐','⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐','⭐⭐⭐⭐⭐'),
    
)
    
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.CharField(max_length=500, default="Lorem, ipsum dolor sit amet consectetur adipisicing elit. Eum laudantium quia nisi optio laborum ut quisquam? Laboriosam labore fugit voluptatibus dicta, praesentium iste placeat, fuga modi dignissimos nesciunt nemo eligendi?")
    image = models.ImageField(upload_to="menu_images")
    category = models.CharField(max_length=50, choices= CATEGORY_CHOICES)
    rate= models.CharField(max_length=10,choices=RATING ,default='in_review')
    

    def __str__ (self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    

    def __str__(self):
        return f"{self.user.username}'s cart - {self.product.name}"

class UserCheckout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    fullname=models.CharField(max_length=100)
    items = models.ManyToManyField(Cart)
    deliveryfee=models.PositiveIntegerField(default=500)
    totalcash = models.IntegerField(default=0)
    email=models.CharField(max_length=100, default="abcd@gmail.com")
    telephone= models.IntegerField()
    shipping_address = models.CharField(max_length=100)
    PAYMENT= (('credit_card', 'Credit Card'), ('paypal', 'PayPal'),('ussd', 'USSD'),('cash', 'Cash'),('bank_transfer', 'Bank Transfer'))
    payment_method = models.CharField(choices=PAYMENT,max_length=100)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return f"UserCheckout for user {self.user.username}"
    

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=100)
    items = models.ManyToManyField(Cart)
    deliveryfee = models.PositiveIntegerField(default=500)
    totalcash = models.IntegerField(default=0)
    email = models.CharField(max_length=100)
    telephone = models.IntegerField()
    shipping_address = models.CharField(max_length=100)
    PAYMENT = (('credit_card', 'Credit Card'), ('paypal', 'PayPal'),('ussd', 'USSD'),('cash', 'Cash'),('bank_transfer', 'Bank Transfer'))
    payment_method = models.CharField(choices=PAYMENT,max_length=100)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"Ordered Items: {self.items} {self.pk}"

    
class Ordered_item(models.Model):
    order = models.ForeignKey(Order, related_name='ordered_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Ordered Items for {self.name}"