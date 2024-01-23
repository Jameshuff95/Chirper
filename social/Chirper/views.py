from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Chirp
from .forms import ChirpForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms

def home(request):
    if request.user.is_authenticated:
        form = ChirpForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                chirp = form.save(commit=False)
                chirp.user = request.user
                chirp.save()
                messages.success(request, ("Your chirp has been posted!"))
                return redirect('home')

        #show all the meeps in order of latest to earliest
        chirps = Chirp.objects.all().order_by("-created_at")
        return render(request, 'home.html', { "chirps":chirps, "form":form })
    else:
        chirps = Chirp.objects.all().order_by("-created_at")
        return render(request, 'home.html', { "chirps":chirps })

def profile_list(request):
    if request.user.is_authenticated:
        # Query the db and put all users on the screen
        # Exclude current user from list with exclude()
        profiles = Profile.objects.exclude(user=request.user)
        # pass the profiles variables into the page within the {}
        return render(request, 'profile_list.html', {'profiles':profiles})
    else: 
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')

# pk means primary key of the user
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        # keep track of your own chirps on profile
        chirps = Chirp.objects.filter(user_id=pk).order_by("-created_at")
        # Post form logic
        if request.method == "POST":
            # Get current user
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            # Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            # Save the profile
            current_user_profile.save()
        return render(request, 'profile.html', {'profile':profile, "chirps":chirps})
    else:
        messages.success(request, ("You must be logged in to view this page."))
        return redirect('home')

def login_user(request):
    # if the form is filled out and posted
    # get the username the user types
    if request.method == "POST":
        # username/password are affiliated with the login form field name
        username = request.POST['username']
        password = request.POST['password']
        # figure out which user is loging in
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in, please try again."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

    
def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have successfully registered!"))
            return redirect('home')
    return render(request, 'register.html', {'form':form})
