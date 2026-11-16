
from django.urls import path
from . import views


urlpatterns = [

    path('', views.register_view, name='home'),

    path('register/', views.register_view, name='register'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard_view, name='dashboard'),

    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'member-dashboard/',
        views.member_dashboard,
        name='member_dashboard'
    ),

    path('profile/', views.profile_view, name='profile'),

    path(
        'profile/edit/',
        views.edit_profile,
        name='edit_profile'
    ),

]
