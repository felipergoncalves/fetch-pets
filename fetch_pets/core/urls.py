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
]