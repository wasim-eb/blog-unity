from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse

class Profile(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
	photo = models.ImageField(upload_to='imgs/', blank=True, null=True)        
	intro = models.TextField(max_length=1000)
	location = models.CharField(max_length=30, blank=True, null=True)
	birth_date = models.DateField(null=True, blank=True)

	def __str__(self):
		return self.user.username

class Category(models.Model):

    name = models.CharField(max_length=10)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
	    verbose_name_plural = 'Categories' 		

class PublishedPostsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class FeaturedPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_featured=True)

class Post(models.Model):

	STATUS_CHOICES = [
        ('draft', 'draft'),
        ('published', 'published'),
    ]
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_posts")
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
	title = models.CharField(max_length=1000)
	description = models.CharField(max_length=1000)
	body = RichTextField()
	slug = models.SlugField(unique=True)
	header_image = models.ImageField(upload_to='imgs/', blank=True, null=True)
	pub_date = models.DateField(auto_now_add=True)
	is_featured = models.BooleanField(default=False)
	status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='draft')
	objects = models.Manager()
	published = PublishedPostsManager()
	featured = FeaturedPostManager()

	def __str__(self):
		return self.title

class Comment(models.Model):

	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")
	comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
	dated = models.DateField(auto_now_add=True)
	body = models.CharField(max_length=500)

	def __str__(self):
		return self.post.title
