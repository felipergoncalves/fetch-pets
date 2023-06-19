from django.contrib import admin
from .models import Profile, Post, Comentario, LikePost, Chat, Message

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comentario)
admin.site.register(LikePost)
admin.site.register(Chat)
admin.site.register(Message)