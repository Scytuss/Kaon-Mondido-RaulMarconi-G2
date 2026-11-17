from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Food, MealLog, DailyCalorieGoal
from .forms import MealLogForm, DailyCalorieGoalForm


@login_required(login_url='login')
def meal_tracker(request):

    today = timezone.localdate()

    # Search Filipino dishes
    search_query = request.GET.get('q', '').strip()

    foods = Food.objects.all()

    if search_query:
        foods = foods.filter(name__icontains=search_query)

    # Get today's meal records
    meal_logs = MealLog.objects.filter(
        user=request.user,
        date_logged__date=today
    ).select_related('food')

    # Calculate daily nutritional totals
    total_calories = Decimal('0')
    total_protein = Decimal('0')
    total_carbohydrates = Decimal('0')
    total_fat = Decimal('0')

    for meal in meal_logs:
        total_calories += meal.total_calories
        total_protein += meal.total_protein
        total_carbohydrates += meal.total_carbohydrates
        total_fat += meal.total_fat

    # Get or create the user's calorie goal
    calorie_goal, created = DailyCalorieGoal.objects.get_or_create(
        user=request.user
    )

    goal_form = DailyCalorieGoalForm(instance=calorie_goal)

    remaining_calories = (
        Decimal(calorie_goal.target_calories) - total_calories
    )

    if calorie_goal.target_calories > 0:
        calorie_percentage = min(
            float(total_calories) / calorie_goal.target_calories * 100,
            100
        )
    else:
        calorie_percentage = 0

    context = {
        'foods': foods,
        'search_query': search_query,
        'meal_logs': meal_logs,

        'meal_form': MealLogForm(),

        'goal_form': goal_form,
        'calorie_goal': calorie_goal,

        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_carbohydrates': total_carbohydrates,
        'total_fat': total_fat,

        'remaining_calories': remaining_calories,
        'calorie_percentage': calorie_percentage,
    }

    return render(request, 'meals/meal_tracker.html', context)


@login_required(login_url='login')
def add_meal(request):

    if request.method == 'POST':
        form = MealLogForm(request.POST)

        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()

            messages.success(
                request,
                f'{meal.food.name} successfully added to your food log!'
            )
        else:
            messages.error(request, 'Please check your meal information.')

    return redirect('meal_tracker')


@login_required(login_url='login')
def update_calorie_goal(request):

    calorie_goal, created = DailyCalorieGoal.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        form = DailyCalorieGoalForm(
            request.POST,
            instance=calorie_goal
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Your calorie goal has been updated.')
        else:
            messages.error(request, 'Please enter a valid calorie goal.')

    return redirect('meal_tracker')


@login_required(login_url='login')
def delete_meal(request, meal_id):

    if request.method == 'POST':
        meal = get_object_or_404(
            MealLog,
            id=meal_id,
            user=request.user
        )

        meal.delete()

        messages.success(request, 'Meal removed from your food log.')

    return redirect('meal_tracker')