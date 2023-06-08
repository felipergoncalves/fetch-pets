from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    nome_usuario = models.CharField(max_length=100, verbose_name='Nome', blank=True, null=True)
    sobrenome_usuario = models.CharField(max_length=100, verbose_name='Sobrenome', blank=True, null=True)
    email = models.EmailField(max_length=100, verbose_name='E-mail', blank=True, null=True)
    cpf = models.CharField(max_length=11, verbose_name='CPF', blank=True, null=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    cep = models.CharField(max_length=8, verbose_name="CEP", blank=True, null=True)
    estado = models.CharField(max_length=100, verbose_name="Estado", blank=True, null=True)
    cidade = models.CharField(max_length=100, verbose_name="Cidade", blank=True, null=True)
    rua = models.CharField(max_length=100, verbose_name="Rua", blank=True, null=True)
    complemento = models.CharField(max_length=100, verbose_name="Complemento", blank=True, null=True)
    numero = models.CharField(max_length=20, verbose_name="Número", blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    descricao = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    especie_animal = models.CharField(max_length=100)
    raca_animal = models.CharField(max_length=100)
    sexo_animal = models.CharField(max_length=100)
    idade = models.IntegerField()
    localizacao = models.CharField(max_length=100)
    #comentarios =
    #favoritos =

    def __str__(self):
        return self.user
