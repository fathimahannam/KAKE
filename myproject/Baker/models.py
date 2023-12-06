# models.py
from django.db import models
from app.models import UserAccount

class Baker(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=255)
    email = models.EmailField()
    image = models.ImageField(upload_to='baker_images', blank=True)
    phoneNumber = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='bakers_images', blank=True)


    

class Cake(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    cakeName = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availableSizes = models.CharField(max_length=255)
    flavors = models.CharField(max_length=255)
    image = models.ImageField(upload_to='cake_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cakeName

class Wishlist(models.Model):
    cake = models.ForeignKey(Cake,on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE)

    def __str__(self):

        return f"{self.cake.cakeName} - {self.user.name}" 

  

    
from django.db import models

class Order(models.Model):
    # Existing fields
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='customer_orders')
    baker = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='baker_orders', null=True)
    product = models.ForeignKey(Cake, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    datetime = models.DateTimeField(auto_now_add=True)

    # New field for order status
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')

    def __str__(self) -> str:
        user_id = getattr(self.user, 'id', None)
        baker_id = getattr(self.baker, 'id', None)
        product_name = getattr(self.product, 'cakeName', None)

        return f"{user_id} - {baker_id} - {product_name} - {self.status}"
