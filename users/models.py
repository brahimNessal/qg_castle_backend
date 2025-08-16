from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model

class User(AbstractUser):
    is_chef = models.BooleanField(default=False)
    is_ingredient_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Dish(models.Model):
    name = models.CharField(max_length=255)
    image = CloudinaryField('image')  # تغيير هنا
    quantity = models.PositiveIntegerField(default=0)
    chef = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dishes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
User = get_user_model()

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    chef = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ingredients')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # احسب السعر الإجمالي تلقائيًا
        self.total_price = (self.quantity or 0) * (self.price_per_unit or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.quantity}"