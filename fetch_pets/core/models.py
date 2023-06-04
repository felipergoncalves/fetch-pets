from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    nome_usuario = models.CharField(max_length=100, verbose_name='Nome')
    sobrenome_usuario = models.CharField(max_length=100, verbose_name='Sobrenome')
    email = models.EmailField(max_length=100, verbose_name='E-mail')
    cpf = models.CharField(max_length=11, verbose_name='CPF')
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')

    def __str__(self):
        return self.user.username