# relationship_app/views/admin_view.py
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render

def is_admin(user):
    return hasattr(user, 'profile') and user.profile.role == 'Admin'

@user_passes_test(is_admin)
@login_required
def admin_dashboard(request):
    return render(request, 'relationship_app/admin_view.html')
