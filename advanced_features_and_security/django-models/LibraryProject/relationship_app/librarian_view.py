# relationship_app/views/librarian_view.py
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render

def is_librarian(user):
    return hasattr(user, 'profile') and user.profile.role == 'Librarian'

@user_passes_test(is_librarian)
@login_required
def librarian_dashboard(request):
    return render(request, 'relationship_app/librarian_dashboard.html')
