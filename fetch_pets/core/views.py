from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
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
    
    
def signin(request):
    if request.method == 'POST':
        usernameSignIn = request.POST['username']
        passwordSignIn = request.POST['password']

        user = auth.authenticate(username=usernameSignIn, password=passwordSignIn)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Dados Inválidos')
            return redirect('login.html')
    else:
        return render(request, 'login.html')
    
def login_view(request):
    if request.method == 'POST':
        if 'signup-form' in request.POST:
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
                    # success
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    # log user in and redirect to settings page

                    # create a profile object for the new user
                    user_model = User.objects.get(username=username)
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                    new_profile.save()
                    return redirect('login')
            else:
                messages.info(request, 'As senhas não são iguais!')
                return redirect('login.html')
        elif 'signin-form' in request.POST:
            usernameSignIn = request.POST['username']
            passwordSignIn = request.POST['password']

            user = auth.authenticate(username=usernameSignIn, password=passwordSignIn)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Dados Inválidos')
                return redirect('login')
    else:
        return render(request, 'login.html')
    
    return HttpResponse('Erro: ação inválida')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')