from django.db import models
from django.conf import settings


class Food(models.Model):
    name = models.CharField(max_length=150, unique=True)
    serving_size = models.CharField(max_length=100)

    calories = models.DecimalField(max_digits=8, decimal_places=2)
    protein = models.DecimalField(max_digits=8, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=8, decimal_places=2)
    fat = models.DecimalField(max_digits=8, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MealLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='meal_logs'
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.PROTECT,
        related_name='meal_logs'
    )

    servings = models.DecimalField(max_digits=6, decimal_places=2, default=1)
    date_logged = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_logged']

    def __str__(self):
        return f"{self.user.username} - {self.food.name}"

    @property
    def total_calories(self):
        return self.food.calories * self.servings

    @property
    def total_protein(self):
        return self.food.protein * self.servings

    @property
    def total_carbohydrates(self):
        return self.food.carbohydrates * self.servings

    @property
    def total_fat(self):
        return self.food.fat * self.servings


class DailyCalorieGoal(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='calorie_goal'
    )

    target_calories = models.PositiveIntegerField(default=2000)

    def __str__(self):
        return f"{self.user.username} - {self.target_calories} calories"