from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator,RegexValidator

#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 Product 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
class Product(models.Model):
    name = models.CharField(max_length=10)
    price = models.IntegerField()
    alchol = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.TextField()  
    place = models.CharField(max_length=10)

    def __str__(self):
        return self.name


#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 Order 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ForeignKey(Product,on_delete=CASCADE, related_name='order_product')
    product_count = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(3)])
    order_time = models.DateTimeField(auto_now_add=True)
    address =  models.CharField(max_length=150)

    class Meta:
        ordering = ['-id']

#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 Weather 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
class City(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, validators = [RegexValidator(r"^[a-zA-Z]+$")])

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'cities'
        ordering = ['-id']