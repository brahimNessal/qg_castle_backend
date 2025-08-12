from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_chef = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Dish(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='dish_images/')
    quantity = models.PositiveIntegerField(default=0)
    chef = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dishes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
