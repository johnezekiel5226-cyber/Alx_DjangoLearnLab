from django.urls import path
from .views import register
from . import views
from .views import (
PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
)

app_name = 'posts'
urlpatterns = [
path('posts/', PostListView.as_view(), name='post-list'),
path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
path("register/", views.register, name="register"),
path("profile/", views.profile, name="profile"),
path("profile/edit/", views.edit_profile, name="edit_profile"),
path('post/new/', views.PostCreateView.as_view(), name='post-create'),
path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
path('<int:post_id>/comments/new/', views.add_comment, name='comment_new'),
path('<int:post_id>/comments/<int:pk>/edit/', views.CommentEditView.as_view(), name='comment_edit'),
path('<int:post_id>/comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]


urlpatterns = [
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),

]
