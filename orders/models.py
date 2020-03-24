from django.db import models
from django.contrib.auth.models import User

# Create your models here.

SIZES = (
    ("s","Small"),
    ("l","Large")
)

STYLES = (
    ('R',"Regular"),
    ('S',"Sicilian")
)

class menu_items(models.Model):
    name=models.CharField(max_length=64)
    description=models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    img_location = models.CharField(max_length=64, default='something')

    def __str__(self):
        return f"{self.name} - {self.price}"

class Order_counter(models.Model):
    counter=models.IntegerField()

    def __str__(self):
        return f"Order no: {self.counter}  "

class User_order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order_number=models.IntegerField()
    status=models.CharField(max_length=64,default='initiated')

    def __str__(self):
        return f"{self.user} - {self.order_number} - {self.status}"

class Cart(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    number=models.IntegerField()
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=7,decimal_places=2)

    def __str__(self):
        return f"{self.name} - ${self.price} "