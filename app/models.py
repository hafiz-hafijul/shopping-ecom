from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator



STATE_CHOICES = [
    ('Rajshahi','Rajshahi'),
    ('Dhaka','Dhaka'),
    ('Chattogram','Chattogram'),
    ('Sylhet','Sylhet'),
    ('Khulna','Khulna'),
    ('Rangpur','Rangpur'),
    ('Barisal','Barisal'),
    ('Mymensingh','Mymensingh'),
]

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zipcode = models.PositiveIntegerField()
    state = models.CharField(max_length=50, choices=STATE_CHOICES)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES = [
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','TopWears'),
    ('BM','Bottomwears'),
]

class Product(models.Model):
    title = models.CharField(max_length=250)
    selling_price=models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=250)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    product_image = models.ImageField(upload_to = 'product_image')

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = [
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivery','Delivery'),
    ('Cancel','Cancel'),
]

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Pending')
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
