from django.urls import path
from . import views

urlpatterns = [
    path('', views.meal_tracker, name='meal_tracker'),

    path('add/', views.add_meal, name='add_meal'),

    path(
        'update-goal/',
        views.update_calorie_goal,
        name='update_calorie_goal'
    ),

    path(
        'delete/<int:meal_id>/',
        views.delete_meal,
        name='delete_meal'
    ),
]