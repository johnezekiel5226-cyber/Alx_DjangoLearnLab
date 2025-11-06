# relationship_app/views/member_view.py
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render

def is_member(user):
    return hasattr(user, 'profile') and user.profile.role == 'Member'

@user_passes_test(is_member)
@login_required
def member_dashboard(request):
    return render(request, 'relationship_app/member_dashboard.html')
