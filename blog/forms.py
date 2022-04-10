from django import forms
from .models import Profile, Post, Comment, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(max_length=200)
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2', 'email']

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['birth_date', 'location', 'photo', 'intro',]


class CreatePostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'category', 'description', 'body', 'header_image', 'status']

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['body']


class Select_Category(forms.Form):
	ctgry = forms.ModelChoiceField(queryset=Category.objects.all())
	class Meta:
		fields = ['ctgry']
