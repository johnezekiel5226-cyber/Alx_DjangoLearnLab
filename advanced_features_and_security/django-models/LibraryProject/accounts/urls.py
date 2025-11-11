from django.urls import path
from . import views

urlpatterns = [
    # You can adjust this later
    path('', views.home_view, name='home'),
]
