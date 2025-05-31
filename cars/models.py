from django.db import models
from brands.models import Brand

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
