import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from .models import Profile, Post, Comentario, LikePost, Chat, Message
from django.db.models import Q

# Create your views here.
def index(request):    
    posts = Post.objects.all()
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        return render(request, 'index.html', {'user_profile': user_profile, 'posts':posts})
    else:
        return render(request, 'index.html', {'posts':posts})
    
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
                    return redirect('login')
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
                return redirect('login')
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

@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='/login')
def profile(request):
    user_profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(user=request.user)
    posts_length = len(posts)
    return render(request, 'profile.html', {'user_profile': user_profile, 'posts':posts, 'posts_length':posts_length})

@login_required(login_url='/login')
def settings(request):  
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
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
        messages.info(request, 'Dados atualizados com sucesso!')
        return redirect('profile')
    return render(request, 'settings.html', {'user_profile': user_profile})  

@login_required(login_url='/login')
def upload(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        descricao = request.POST['descricao']
        especie = request.POST['especie']
        raca = request.POST['raca']
        sexo = request.POST['sexo']
        idade = request.POST['idade']
        localizacao = request.POST['localizacao']

        new_post = Post.objects.create(user=user, image=image, descricao=descricao, especie_animal=especie, raca_animal=raca, sexo_animal=sexo, idade=idade, localizacao=localizacao)
        new_post.save()

        messages.info(request, 'Post criado com sucesso!')
        return redirect('/')    
    return render(request, 'pet-form.html', {'user_profile':user_profile})
  
@login_required(login_url='/login')
def petPage(request, pk):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    post = Post.objects.get(id=pk)
    post_owner = User.objects.get(username=post.user)
    post_owner_profile = Profile.objects.get(user=post_owner)
    comentarios = post.comentarios_relacionados.all()

    username=request.user
    #armazenar o post para verificar se o usuário já curtiu
    likedPost = LikePost.objects.filter(post_id=post, username=username)
    change_color = False
    if likedPost:
        change_color = True
        print("Achou")

    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'post':post,
        'post_owner_profile':post_owner_profile,
        'comentarios':comentarios,
        'change_color':change_color
    }

    if request.method == 'POST':
         # Obtenha os dados do formulário de comentário submetido
        conteudo = request.POST.get('conteudo')
        post_id = pk

        # Obtenha o post relacionado ao comentário
        post = Post.objects.get(id=post_id)

        # Obtenha o usuário logado
        autor = request.user

        # Obtenha as informações do autor do perfil
        profile = Profile.objects.get(user=autor)
        nome_autor = f"{profile.nome_usuario} {profile.sobrenome_usuario}"
        imagem_autor = profile.profileimg

        # Crie o comentário
        comentario = Comentario.objects.create(
            post=post,
            autor=autor,
            conteudo=conteudo,
            nome_autor=nome_autor,
            imagem_autor=imagem_autor
        )

    return render(request, 'pet-page.html', context)

@login_required(login_url='/login')
def like(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    current_likes = post.likes
    liked = LikePost.objects.filter(username=user, post_id=post).count()
    if not liked:
        liked = LikePost.objects.create(username=user, post_id=post)
        current_likes = current_likes + 1
    else:
        liked = LikePost.objects.filter(username=user, post_id=post).delete()
        current_likes = current_likes - 1
    post.likes = current_likes
    post.save()
    return redirect(f'/pet-page/{pk}')

@login_required(login_url='/login')
def liked_posts(request):
    user_profile = Profile.objects.get(user=request.user)
    user = request.user
    liked_posts = LikePost.objects.filter(username=user).values('post_id')
    posts = Post.objects.filter(id__in=liked_posts)
    posts_length = len(posts)
    context = {
        'user_profile': user_profile,
        'liked_posts': posts,
        'posts_length':posts_length
    }

    return render(request, 'liked_posts.html', context)

@login_required
def create_chat(request, user_id):
    # Verifica se o usuário dono do post existe
    post_owner = get_object_or_404(User, username=user_id)

    # Verifica se já existe um chat entre o usuário logado e o usuário dono do post
    chat = Chat.objects.filter(Q(user1=request.user, user2=post_owner) | Q(user1=post_owner, user2=request.user)).first()

    # Se não existir um chat, cria um novo
    if not chat:
        chat = Chat.objects.create(user1=request.user, user2=post_owner)

    return redirect(f'/chat/{chat.id}')


def chat_detail(_request, chat_id=None):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.all() if chat else None

    chat_data = {
        'chat_id': chat.id,
        'user2_username': chat.user2.username if chat else None,
        'messages': [{'content': message.content, 'timestamp': message.timestamp} for message in messages] if messages else None,
    }
    return JsonResponse(chat_data)

@login_required(login_url='/login')
def chats(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    # Obtém todos os chats do usuário logado
    user_chats = Chat.objects.filter(Q(user1=request.user) | Q(user2=request.user))

    context = {
        'chats': [{'id': user_chat.id, 'user1': user_chat.user1, 'user2': user_chat.user2, 'user1_profile': Profile.objects.get(user=user_chat.user1), 'user2_profile': Profile.objects.get(user=user_chat.user2)} for user_chat in user_chats] if user_chats else None,
        'user_object':user_object,
        'user_profile':user_profile,
    }

    print(user_chats)

    return render(request, 'chat.html', context)
    
@login_required(login_url='/login')
def chats_view(request,  chat_id=None):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    query_set = Chat.objects.filter(Q(id=chat_id, user1=request.user) | Q(id=chat_id, user2=request.user))
    chat = get_object_or_404(query_set)
    # Obtém todos os chats do usuário logado
    user_chats = Chat.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    messages = chat.messages.all() if chat else None
    user_to_display = chat.user2.username
    if chat.user2.username == request.user.username:
        user_to_display = chat.user1.username
    user_chat_object = User.objects.get(username=user_to_display)
    user_chat_profile = Profile.objects.get(user=user_chat_object)
    

    chat_data = {
        'chats':  [{'id': user_chat.id, 'user1': user_chat.user1, 'user2': user_chat.user2, 'user1_profile': Profile.objects.get(user=user_chat.user1), 'user2_profile': Profile.objects.get(user=user_chat.user2)} for user_chat in user_chats] if user_chats else None,
        'chat_id': chat.id,
        'user_object':user_object,
        'user_profile':user_profile,
        'user_chat_object':user_chat_object,
        'user_chat_profile':user_chat_profile,
        'messages': [{'content': message.content, 'timestamp': message.timestamp} for message in messages] if messages else None,
    }
    return render(request, 'chat.html', chat_data)

      

def send_message(request, chat_id):
    if request.method == 'POST':
        # Verifique se o chat existe
        chat = get_object_or_404(Chat, id=chat_id)

        print('Mostrando o chat', chat)
        
        # Obtenha o conteúdo da mensagem enviado pelo formulário
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['content']
        
        # Crie uma nova mensagem
        message = Message(chat=chat, sender=request.user, content=content)
        message.save()

        # Retorne a resposta JSON com os dados da nova mensagem
        response_data = {
            'content': message.content,
            'timestamp': message.timestamp,
        }
        return JsonResponse(response_data)

    # Se a requisição não for um POST, retorne uma resposta de erro
    return JsonResponse({'error': 'Método inválido.'})