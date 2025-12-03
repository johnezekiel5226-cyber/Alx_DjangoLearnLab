from django.views.generic import
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm




class PostListView(ListView):
model = Post
template_name = 'posts/post_list.html' # app/templates/posts/post_list.html
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
# set current user as the author
form.instance.author = self.request.user
return super().form_valid(form)




class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
model = Post
form_class = PostForm
template_name = 'posts/post_form.html'


def test_func(self):
post = self.get_object()
return post.author == self.request.user




class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
model = Post
template_name = 'posts/post_confirm_delete.html'
success_url = reverse_lazy('posts:post-list')


def test_func(self):
post = self.get_object()
return post.author == self.request.user
