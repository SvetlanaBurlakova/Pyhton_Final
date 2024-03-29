from django.db import models
from django.utils import timezone

from user.models import User
from django.contrib.auth import get_user_model
#
#
User = get_user_model()

# Create your models here.
# class User(AbstractUser):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField()
#     registration_date = models.DateField(default=timezone.now)

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    measurement_type = models.CharField(max_length=10)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}, {self.measurement_type}'



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    steps = models.TextField(max_length=1000)
    cooking_time = models.DurationField(default=0)
    image = models.ImageField(upload_to='recipes/', default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, through="IngredientInfo")
    category = models.ManyToManyField(Category)

    def __str__(self):
        return f'{self.name} {self.category}'


class IngredientInfo(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)














