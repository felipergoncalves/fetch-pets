from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout, name='logout'),
    path('myprofile', views.myprofile, name='myprofile'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload')
]