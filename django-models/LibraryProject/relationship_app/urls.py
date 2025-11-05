from django.urls import path
from . import views
from .views import book_list, LibraryDetailView
from .views import list_books
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Book and Library URLs
    path('books/', views.book_list, name='book_list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='book_list'), name='logout'),
    path('register/', views.register, name='register'),
    # Logout view using Django's built-in LogoutView
    path('logout/', auth_views.LogoutView.as_view(next_page='book_list'), name='logout'),
    # Registration view (custom function-based view)
    path('register/', views.register, name='register'),
]
