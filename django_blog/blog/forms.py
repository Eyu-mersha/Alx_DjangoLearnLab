from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.author = self.user  # Associate the logged-in user as the author
            post.save()
        return post
