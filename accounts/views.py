
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import (
    RegistrationForm,
    UserProfileForm,
    ProfileForm
)


# REGISTRATION
def register_view(request):

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Your Kaon account has been created successfully!"
            )

            return redirect('login')

    else:

        form = RegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


# LOGIN
def login_view(request):

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            messages.success(
                request,
                "Welcome back to Kaon!"
            )

            return redirect('dashboard')

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    else:

        form = AuthenticationForm()

    return render(
        request,
        'accounts/login.html',
        {'form': form}
    )


# LOGOUT
@login_required
@require_POST
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have successfully logged out."
    )

    return redirect('login')


# DASHBOARD REDIRECT
@login_required
def dashboard_view(request):

    if request.user.profile.role == 'ADMIN':

        return redirect('admin_dashboard')

    return redirect('member_dashboard')


# ADMIN DASHBOARD
@login_required
def admin_dashboard(request):

    if request.user.profile.role != 'ADMIN':

        messages.error(
            request,
            "You are not authorized to access the Admin Dashboard."
        )

        return redirect('member_dashboard')

    return render(
        request,
        'accounts/admin_dashboard.html'
    )


# MEMBER DASHBOARD
@login_required
def member_dashboard(request):

    if request.user.profile.role != 'MEMBER':

        messages.error(
            request,
            "You are not authorized to access the Member Dashboard."
        )

        return redirect('admin_dashboard')

    return render(
        request,
        'accounts/member_dashboard.html'
    )


# VIEW PROFILE
@login_required
def profile_view(request):

    return render(
        request,
        'accounts/profile.html',
        {
            'user': request.user,
            'profile': request.user.profile,
            'edit_mode': False
        }
    )


# EDIT PROFILE
@login_required
def edit_profile(request):

    user = request.user
    profile = user.profile

    if request.method == 'POST':

        user_form = UserProfileForm(
            request.POST,
            instance=user
        )

        profile_form = ProfileForm(
            request.POST,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            messages.success(
                request,
                "Your profile has been updated successfully!"
            )

            return redirect('profile')

    else:

        user_form = UserProfileForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(
        request,
        'accounts/profile.html',
        {
            'user': user,
            'profile': profile,
            'user_form': user_form,
            'profile_form': profile_form,
            'edit_mode': True
        }
    )
