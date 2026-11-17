from django.contrib import admin
from .models import Food, MealLog, DailyCalorieGoal


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'serving_size',
        'calories',
        'protein',
        'carbohydrates',
        'fat',
    )

    search_fields = ('name',)
    ordering = ('name',)


@admin.register(MealLog)
class MealLogAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'food',
        'servings',
        'date_logged',
    )

    list_filter = ('date_logged',)
    search_fields = ('user__username', 'food__name')


@admin.register(DailyCalorieGoal)
class DailyCalorieGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_calories')
    search_fields = ('user__username',)