from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('pet-page/<str:pk>', views.petPage, name='pet-page'),
    path('like/<str:pk>', views.like, name='like'),
    path('liked_posts', views.liked_posts, name='liked_posts'),
    path('chats', views.chats, name="chats"),
    path('chat/<int:chat_id>', views.chats_view, name="chat"),
    path('create_chat/<str:user_id>/', views.create_chat, name='create_chat'),
    path('chat_detail/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('send_message/<int:chat_id>/', views.send_message, name='send_message'),
    path('edit_post/<uuid:id>', views.editPost, name='edit_post'),
    path('excluir_post/<uuid:id>/', views.excluir_post, name='excluir_post')
]