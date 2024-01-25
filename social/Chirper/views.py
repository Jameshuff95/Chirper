""" All comments above each definition appear in order from top to bottom as written """

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Chirp
from .forms import ChirpForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


# chirps shows all the meeps in order of latest to earliest
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
        chirps = Chirp.objects.all().order_by("-created_at")
        return render(request, 'home.html', { "chirps":chirps, "form":form })
    else:
        chirps = Chirp.objects.all().order_by("-created_at")
        return render(request, 'home.html', { "chirps":chirps })


# profiles will query the db and put all users on the screen
# it will also exclude current user from list with exclude()
# return render() will pass the profiles variables into the page within the {}
def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profiles':profiles})
    else: 
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')


# pk in profile() means primary key of the user
# chirps will keep track of your own chirps on profile
# current_user_profile gets current user
# action gets form data
# if action: means to decide to follow or unfollow
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        chirps = Chirp.objects.filter(user_id=pk).order_by("-created_at")
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request, 'profile.html', {'profile':profile, "chirps":chirps})
    else:
        messages.success(request, ("You must be logged in to view this page."))
        return redirect('home')


# if the form is filled out and posted
# get the username the user types
# username/password are affiliated with the login form field name
# user figures out which user is logging in
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
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

# user logs in the user
def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have successfully registered!"))
            return redirect('home')
    return render(request, 'register.html', {'form':form})

# current_user grabs the current user
# profile_user display the current user profile
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, ("You have successfully updated your account!"))
            return redirect('home')
        return render(request, 'update_user.html', {"user_form":user_form, "profile_form":profile_form})
    else:
        messages.success(request, ("You must be logged in to view this page!"))
        return redirect('login')
