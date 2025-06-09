from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Post, Comment

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class LoginForm(AuthenticationForm):
    # Можно не переопределять поля: оставляем стандартные username и password.
    pass


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }
