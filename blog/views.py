from unicodedata import category
from django.shortcuts import render, redirect
from .models import Profile, Post, Comment, Category
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm, CreatePostForm, CommentForm, Select_Category
from django.contrib.auth import authenticate, login

def index(request):
	ctgry = None
	categry = None
	featured_post = Post.featured.all().order_by('-pub_date')[0]
	posts = Post.published.all().order_by('-pub_date')[:5]
	form = Select_Category()
	if request.method == 'POST':
		form = Select_Category(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			ctgry = cd['ctgry']
			categry = Category.objects.get(name=ctgry)
			posts = Post.published.filter(category=categry).order_by('-pub_date')[:5]		
	
	context = {
		'featured_post': featured_post,
		'posts': posts,
		'form': form,
	}
	return render(request, 'blog/index.html', context)

def archives(request):
	ctgry = None
	categry = None
	posts = Post.published.all().order_by('-pub_date')
	form = Select_Category()
	if request.method == 'POST':
		form = Select_Category(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			ctgry = cd['ctgry']
			categry = Category.objects.get(name=ctgry)
			posts = Post.published.filter(category=categry).order_by('-pub_date')[:5]
	context = {
		'posts' : posts,
		'form': form,
	}
	return render (request, 'blog/archives.html', context)

def search(request):
	if request.method == 'GET':
		posts = []
		searched = request.GET.get('searched', None)
		if searched:
			posts = Post.objects.filter(title__contains=searched)
	context = {
		'searched' : searched,
		'posts' : posts,
	}	
	return render(request, 'blog/search.html', context)

def signup(request):

	form1 = CustomUserCreationForm()
	form2 = ProfileForm()

	if request.method == 'POST':
		form1 = CustomUserCreationForm(request.POST)
		form2 = ProfileForm(request.POST, request.FILES)
		
		if form1.is_valid():
			
			new_user = form1.save()
			new_user = authenticate(
				username=form1.cleaned_data['username'], password=form1.cleaned_data['password1'],
			)
			login(request, new_user)

		if form2.is_valid():

			# Configuration for Profile form
			instance = form2.save(commit=False)
			instance.user = request.user
			image = form2.cleaned_data['photo']
			instance.photo = image
			instance.save()

		return redirect('index')
	
	else:
		form1 = CustomUserCreationForm()
		form2 = ProfileForm()
					
	context = {
		'form1' : form1,
		'form2' : form2,
	}
	return render(request, 'registration/signup.html', context)

def create_post(request):

	form = CreatePostForm()
	if request.method == "POST":
		form = CreatePostForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.profile = request.user.profile
			image = form.cleaned_data['header_image']
			instance.category = form.cleaned_data['category']
			instance.header_image = image
			instance.save()

			return redirect('profile_page')
	else:
		form = CreatePostForm()

	context = {
		'form': form,
	}
	return render(request, 'blog/create_post.html', context)

def detail(request, post_id):

	post = Post.objects.get(id=post_id)
	profile = Profile.objects.get(user=post.author)
	user_posts = Post.objects.filter(author=post.author, status='published').exclude(id=post.id)
	comments = Comment.objects.filter(post=post).order_by('-dated')[:5]

	form = CommentForm()
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.comment_by = request.user
			instance.post = post
			instance.save()
			return redirect(request.path)
		else:
			print("Not ok")
			print(form.errors)
	context = {
		'post': post,
		'profile': profile,
		'user_posts': user_posts,
		'comments': comments,
		'form': form,
	}
	return render(request, 'blog/detail.html', context)


def edit_post(request, post_id):
	
	post = Post.objects.get(id=post_id)
	form = CreatePostForm(instance=post)
	if request.method == "POST":
		form = CreatePostForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			editted_post = form.save(commit=False)
			editted_post.author = request.user
			image = form.cleaned_data['header_image']
			editted_post.header_image = image
			editted_post.save()
		else:
			print("Not ok")
			print(form.errors)
		return redirect('profile_page')
	context = {
		'form': form,
	}
	return render(request, 'blog/edit_post.html', context)

def delete_post(request, post_id):
	
	post = Post.objects.get(id=post_id)
	post.delete()
	return redirect('profile_page')

def profile_page(request, profile_id=None):
	if profile_id:
		profile = Profile.objects.get(id=profile_id)
	elif request.user.is_authenticated:
		profile = Profile.objects.get(user=request.user)
	draft_posts = Post.objects.filter(author=profile.user, status='draft').order_by('-pub_date')
	published_posts = Post.objects.filter(author=profile.user, status='published').order_by('-pub_date')	
	context = {
		'profile': profile,
		'd_posts': draft_posts,
		'pub_posts': published_posts,
	}
	return render(request, 'blog/profile.html', context)

def edit_profile(request, profile_id):

	profile = Profile.objects.get(id=profile_id)
	form = ProfileForm(instance=profile)
	if request.method == "POST":
		form = ProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			editted_profile = form.save(commit=False)
			editted_profile.user = request.user
			image = form.cleaned_data['photo']
			editted_profile.photo = image
			editted_profile.save()
			return redirect('profile_page')
		else:
			print("Not ok")
			print(form.errors)
	
	context = {
		'form': form,
	}
	return render(request, 'blog/edit_profile.html', context)

