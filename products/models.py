from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name