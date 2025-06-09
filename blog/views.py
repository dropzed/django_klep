from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Post, Comment
from .forms import RegistrationForm, LoginForm, PostForm, CommentForm

def post_list(request):
    """
    Главная страница: список всех постов, отсортированных по дате создания (сначала новые).
    """
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    """
    Просмотр отдельного поста: показываем заголовок, контент, список комментариев и форму добавления нового комментария.
    Если POST-запрос и пользователь аутентифицирован — сохраняем комментарий.
    """
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('created_at')
    new_comment = None

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Только зарегистрированные пользователи могут оставлять комментарии.')
            return redirect('blog:login')  # или просто reload
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Ваш комментарий был опубликован.')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required(login_url='blog:login')
def post_create(request):
    """
    Создание нового поста. Доступно только зарегистрированным.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'Пост успешно создан.')
            return redirect('blog:post_detail', pk=new_post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'is_edit': False})


@login_required(login_url='blog:login')
def post_edit(request, pk):
    """
    Редактирование существующего поста. Убедимся, что текущий пользователь — автор.
    """
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'Вы не можете редактировать чужой пост.')
        return redirect('blog:post_detail', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост успешно обновлён.')
            return redirect('blog:post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'is_edit': True})


def register_view(request):
    """
    Регистрация нового пользователя.
    """
    if request.user.is_authenticated:
        return redirect('blog:post_list')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно. Вы вошли в систему.')
            return redirect('blog:post_list')
    else:
        form = RegistrationForm()
    return render(request, 'blog/register.html', {'form': form})


def login_view(request):
    """
    Вход существующего пользователя.
    """
    if request.user.is_authenticated:
        return redirect('blog:post_list')

    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('blog:post_list')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})


@login_required(login_url='blog:login')
def logout_view(request):
    """
    Выход текущего пользователя.
    """
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('blog:post_list')
