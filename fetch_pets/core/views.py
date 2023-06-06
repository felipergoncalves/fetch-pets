from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Profile

# Create your views here.
def index(request):
    return render(request, 'index.html')
    
        
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
                    user_login = auth.authenticate(username=username, password=password)
                    auth.login(request, user_login)

                    # create a profile object for the new user
                    user_model = User.objects.get(username=username)
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                    new_profile.save()
                    return redirect('settings')
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

@login_required(login_url='login')
def myprofile(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'myprofile.html', {'user_profile': user_profile})

@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            nome = request.POST['nome']
            sobrenome = request.POST['sobrenome']
            cpf = request.POST['cpf']
            email = request.POST['email']
            cep = request.POST['cep']
            estado = request.POST['estado']
            cidade = request.POST['cidade']
            rua = request.POST['rua']
            complemento = request.POST['complemento']
            numero = request.POST['numero']

            user_profile.profileimg = image
            user_profile.nome_usuario = nome
            user_profile.sobrenome_usuario = sobrenome
            user_profile.cpf = cpf
            user_profile.email = email
            user_profile.cep = cep
            user_profile.estado = estado
            user_profile.cidade = cidade
            user_profile.rua = rua
            user_profile.complemento = complemento
            user_profile.numero = numero
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            nome = request.POST['nome']
            sobrenome = request.POST['sobrenome']
            cpf = request.POST['cpf']
            email = request.POST['email']
            cep = request.POST['cep']
            estado = request.POST['estado']
            cidade = request.POST['cidade']
            rua = request.POST['rua']
            complemento = request.POST['complemento']
            numero = request.POST['numero']

            user_profile.profileimg = image
            user_profile.nome_usuario = nome
            user_profile.sobrenome_usuario = sobrenome
            user_profile.cpf = cpf
            user_profile.email = email
            user_profile.cep = cep
            user_profile.estado = estado
            user_profile.cidade = cidade
            user_profile.rua = rua
            user_profile.complemento = complemento
            user_profile.numero = numero
            user_profile.save()
        return redirect('myprofile')

    return render(request, 'settings.html', {'user_profile': user_profile})