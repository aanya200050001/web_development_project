from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Repository


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect('login')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegistrationForm
    return render(request = request, template_name="registration/signup.html", context={"form" : form})

def homepage(request):
	users = User.objects.all()
	return render(request=request, template_name="users.html", context={'users':users})

def view_profile(request, pk=None):
    repos = []
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    repos = Repository.objects.filter(profile = user.profile).order_by('-no_of_stars')

    
    args = {'user_profile': user, "repos" : repos}
    return render(request, 'profile.html', args)

def user_profile(request):
    
    user = User.objects.get(username = request.user)
    repos = Repository.objects.filter(profile = user.profile).order_by('-no_of_stars')
    args = {'user_profile': user, "repos" : repos}
    return render(request, 'profile.html', args)


def update_profile(request):
    
    user = request.user
    user.save()
    repos = Repository.objects.filter(profile = user.profile)
    args = {'user_profile': user, "repos" : repos}
    return render(request, 'profile.html', args)