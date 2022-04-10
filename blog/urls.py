from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('archives/', views.archives, name='archives'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('new_post/', views.create_post, name='create_post'),
    path('post_detail/<int:post_id>/', views.detail, name='detail'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete'),
    path('user_profile/', views.profile_page, name='profile_page'),
    path('user_profile/<int:profile_id>/', views.profile_page, name='user_page'), #To see profiles of authors.
    path('edit_profile/<int:profile_id>/', views.edit_profile, name='edit_profile'),
]
