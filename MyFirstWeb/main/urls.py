from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('users/', views.users_show, name='users_show'),
    path('users/create', views.create_user, name='create_user'),
    path('groups/create', views.create_group, name='create_group'),
    path('groups/', views.groups_show, name='groups_show'),
    path('posts/', views.posts_show, name='posts_show'),
    path('posts/create', views.create_post, name='create_post'),
]