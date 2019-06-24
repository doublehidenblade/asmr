from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('play', views.play, name='play'),
    path('register/', views.register, name='register'),
    path('makepay/', views.makepay, name='makepay'),
    path('handler/', views.handler, name='handler'),
]