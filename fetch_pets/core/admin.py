from django.contrib import admin
from .models import Profile, Post, Comentario

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comentario)