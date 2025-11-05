from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Book and Library Views
    path('books/', views.book_list, name='book_list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Authentication Views
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),

    # Logout view with a template instead of redirect
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Registration view (custom)
    path('register/', views.register, name='register'),
]

