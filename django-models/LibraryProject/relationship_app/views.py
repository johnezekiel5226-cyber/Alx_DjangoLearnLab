# relationship_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Library, UserProfile

# -------------------------------
# Book and Library Views
# -------------------------------
def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})

from django.views.generic import DetailView

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'


# -------------------------------
# Authentication Views
# -------------------------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Profile is auto-created via signal
            login(request, user)
            # Redirect based on role (default 'Member')
            if hasattr(user, 'profile'):
                role = user.profile.role
                if role == 'Admin':
                    return redirect('admin_dashboard')
                elif role == 'Librarian':
                    return redirect('librarian_dashboard')
                else:
                    return redirect('member_dashboard')
            return redirect('member_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# -------------------------------
# Role Check Helper Functions
# -------------------------------
def is_admin(user):
    return hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'profile') and user.profile.role == 'Member'


# -------------------------------
# Role-Based Dashboard Views
# -------------------------------
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required
@user_passes_test(is_librarian)
def librarian_dashboard(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required
@user_passes_test(is_member)
def member_dashboard(request):
    return render(request, 'relationship_app/member_view.html')
