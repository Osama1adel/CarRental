from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from bookings.models import Booking
from .forms import UserUpdateForm, ProfileUpdateForm 
from django.db import transaction 


@login_required
def profile_view(request):
    
    # Ensure a profile exists for the user
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Initialize forms for profile update
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=profile)

    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    context = {
        "bookings": bookings,
        "user": request.user,
        "user_form": user_form,       
        "profile_form": profile_form,   
        "profile_instance": profile,    
    }
    return render(request, "accounts/profile.html", context)


@login_required
@transaction.atomic 
def update_profile(request):

    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account details have been updated successfully.', 'success')
            return redirect('accounts:profile')
        
        else:
            messages.error(request, 'There was an error in the submitted data. Please review the fields.', 'danger')

    return redirect('accounts:profile') 



@login_required
@transaction.atomic
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request) # Log out the user before deleting to prevent session errors
        user.delete() 
        messages.success(request, 'Your account has been successfully deleted.', 'success')
        return redirect('main:home')
        
    return redirect('accounts:profile')



def login_view(request): 
    if request.method == "POST": 
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully", "alert-success")
            
            if user.is_staff:
                return redirect('bookings:reviewer_dashboard')
            
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            
            return redirect('main:home') 
        
        else:
            messages.error(request, "Email or Password doesn't match!", "alert-danger")

    return render(request, "accounts/login.html")


def register_view(request): 
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        password_confirm = request.POST["password2"]

        if password != password_confirm:
            messages.error(request, "Passwords don't match!", "danger")
            return render(request, "accounts/registration.html")

        if User.objects.filter(username=email).exists():
            messages.error(request, "This email is already registered!", "danger")
            return render(request, "accounts/registration.html")

        try:
            new_user = User.objects.create_user(
                username=email,  
                email=email,
                password=password,
                first_name=username
            )
            new_user.save()
            
            messages.success(request, "Registration Successful, please login.", "success")
            return redirect("accounts:login")

        except Exception as e:
            print(e)
            messages.error(request, "Something went wrong during registration.", "danger")

    return render(request, "accounts/registration.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out Successfully", "success")
    return redirect("main:home") 