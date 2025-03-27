from django.db import models
from django.core.validators import MinValueValidator 

# Create your models here.

# many to many relation
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    def __str__(self):
        return self.description  + self.discount
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey("Product",on_delete=models.SET_NULL,null=True,blank=True,related_name="+")
    def __str__(self):
        return self.title 
    class Meta:
        ordering=["title"]

class Product(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2,validators=[MinValueValidator(1)])
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT)
    def __str__(self):
        return self.title
    class Meta:
        ordering= ["-id"]



class Customer(models.Model):
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"
    MEMBERSHIP_CHOICES= [
        (MEMBERSHIP_BRONZE,"Bronze"),
        (MEMBERSHIP_SILVER,"Silver"),
        (MEMBERSHIP_GOLD,"Gold")
    ]
    first_name = models.CharField(max_length=255)
    last_name  = models.CharField(max_length=255)
    email = models.EmailField(max_length=254,unique=True)
    birth_date = models.DateField(null = True)
    phone = models.CharField(max_length=255,unique=True,validators=[])
    membership = models.CharField(max_length = 1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        ordering = ["first_name","last_name"]

class Order(models.Model):
    PAYMENT_PENDING = "P"
    PAYMENT_COMPLETED = "C"
    PAYMENT_FAILED = "F"
    PAYMENT_CHOICE = [
        (PAYMENT_COMPLETED,"Completed"),
        (PAYMENT_PENDING,"Pending"),
        (PAYMENT_FAILED,"Failed")
    ] 
    placed_at  = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_CHOICE,default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)
    def __str__(self):
        return self.payment_status
    class Meta:
        ordering = ["placed_at"]
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE) 
    quantity = models.PositiveSmallIntegerField()
class OrderItem(models.Model):
    quantity = models.PositiveSmallIntegerField()
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    product  = models.ForeignKey(Product,on_delete=models.PROTECT, related_name="orderitem")
    unit_price = models.DecimalField(max_digits=6,decimal_places=2) 
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    # one to one
    # customer = models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True)
    # one to many
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)

class Review(models.Model):
    product  = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="reviews")
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)