from django.contrib import admin
from .models import Profile, Post, Comment, Category

class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'birth_date']

admin.site.register(Profile, ProfileAdmin)


class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'category', 'author', 'pub_date', 'status', 'is_featured']
	prepopulated_fields = {"slug": ("title",)}
	list_filter = ('title', 'author', 'pub_date')
	list_editable = ['status', 'is_featured']

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
	list_display = ['post', 'comment_by']

admin.site.register(Comment, CommentAdmin)


class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name',]
	prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)
