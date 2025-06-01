from django.db import models
from brands.models import Brand
from django.contrib.auth.models import User
from django.utils import timezone


class Car(models.Model):
    image = models.ImageField(upload_to='cars/')
    model = models.CharField(max_length=100)
    
    CAR_STATUS_CHOICES = [
        ('new', 'Brand New'),
        ('used', 'Pre-Owned'),
    ]
    status = models.CharField(max_length=10, choices=CAR_STATUS_CHOICES)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.brand.name} {self.model}"

class Comment(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    guest_name = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        name = self.user.username if self.user else self.guest_name
        return f"Comment by {name} on {self.car}"

class Purchase(models.Model):
    PAYMENT_METHODS = [        
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('rocket', 'Rocket'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='bkash')
    shipping_address = models.TextField()
    purchase_date = models.DateTimeField(default=timezone.now)