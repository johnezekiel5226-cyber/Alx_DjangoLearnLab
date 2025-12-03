from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.views.generic import (
ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm



@login_required
def profile(request):
    return render(request, "blog/profile.html")

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # automatically login user after registration
            return redirect("home")  # redirect to your homepage
    else:
        form = CustomUserCreationForm()

    return render(request, "blog/register.html", {"form": form})

class PostListView(ListView):
model = Post
template_name = 'posts/post_list.html'
context_object_name = 'posts'
paginate_by = 10

class PostDetailView(DetailView):
model = Post
template_name = 'posts/post_detail.html'
context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
model = Post
form_class = PostForm
template_name = 'posts/post_form.html'


def form_valid(self, form):
form.instance.author = self.request.user
return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
model = Post
form_class = PostForm
template_name = 'posts/post_form.html'


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
model = Post
template_name = 'posts/post_confirm_delete.html'
success_url = reverse_lazy('posts:post-list')


def test_func(self):
post = self.get_object()
return post.author == self.request.user



@login_required
def edit_profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }

    return render(request, "blog/edit_profile.html", context)
