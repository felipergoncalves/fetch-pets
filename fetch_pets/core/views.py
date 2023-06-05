from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.http import HttpResponse
from .models import Profile

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username-signup']
        email = request.POST['email-signup']
        password = request.POST['password-signup']
        password2 = request.POST['password-confirm']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email já está cadastrado!')
                return redirect('login.html')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username já existe!')
                return redirect('login')
            else:
                #success
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                #log user in and redirect to settings page

                #create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('login')
        else:
            messages.info(request, 'As senhas não são iguais!')
            return redirect('login.html')
    else:
        return render(request, 'login.html')