from django import forms
from .models import MealLog, DailyCalorieGoal


class MealLogForm(forms.ModelForm):

    class Meta:
        model = MealLog
        fields = ['food', 'servings']

        widgets = {
            'food': forms.Select(attrs={
                'class': 'form-input'
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0.01',
                'step': '0.01',
                'placeholder': 'Number of servings'
            }),
        }

        labels = {
            'food': 'Select Filipino Dish',
            'servings': 'Number of Servings',
        }


class DailyCalorieGoalForm(forms.ModelForm):

    class Meta:
        model = DailyCalorieGoal
        fields = ['target_calories']

        widgets = {
            'target_calories': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '1',
                'placeholder': 'Enter your daily calorie goal'
            }),
        }

        labels = {
            'target_calories': 'Daily Calorie Goal'
        }