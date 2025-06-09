from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Главная страница — список всех постов
    path('', views.post_list, name='post_list'),

    # Регистрация и вход/выход
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Страница создания нового поста
    path('post/new/', views.post_create, name='post_create'),
    # Редактирование поста: передаём ID
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),

    # Просмотр отдельного поста (и его комментариев)
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]
