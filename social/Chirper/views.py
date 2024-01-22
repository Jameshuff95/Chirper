from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def profile_list(request):
    if request.user.is_authenticated:
        # Query the db and put all users on the screen
        # Exclude current user from list with exclude()
        profiles = Profile.objects.exclude(user=request.user)
        # pass the profiles variables into the page within the {}
        return render(request, 'profile_list.html', {"profiles":profiles})
    else: 
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')

# pk means primary key of the user
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        return render(request, 'profile.html', {'profile':profile})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')
