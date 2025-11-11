from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import admin_view, librarian_view, member_view

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
    path('admin-dashboard/', admin_view.admin_dashboard, name='admin_dashboard'),
    path('librarian-dashboard/', librarian_view.librarian_dashboard, name='librarian_dashboard'),
    path('member-dashboard/', member_view.member_dashboard, name='member_dashboard'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
]




