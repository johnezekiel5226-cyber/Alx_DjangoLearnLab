from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Post, Tag
from django.utils.text import slugify


class PostForm(forms.ModelForm):
     tags = forms.CharField(required=False, help_text="Comma-separated tags")
class Meta:
     model = Post
     fields = ['title', 'content', 'slug', 'tags']
     widgets = {
     'title': forms.TextInput(attrs={'class': 'form-control'}),
     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
      }

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows':3, 'placeholder': 'Write a thoughtful comment...'}),
        max_length=2000,
        label='',
    )

    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        if len(content) < 2:
            raise forms.ValidationError("Comment is too short.")
        return content

    def __init__(self, *args, **kwargs):
        # if editing, prepopulate tags field
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {})
        if instance:
            initial['tags'] = ', '.join(t.name for t in instance.tags.all())
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

     class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_tags(self):
        data = self.cleaned_data.get('tags', '')
        # normalize and return list of names
        names = [t.strip() for t in data.split(',') if t.strip()]
        return names

    def save(self, commit=True):
        names = self.cleaned_data.pop('tags', [])
        post = super().save(commit=commit)
        # create or get tags then set m2m
        tag_objs = []
        for name in names:
            slug = slugify(name)
            tag_obj, _ = Tag.objects.get_or_create(name=name, defaults={'slug': slug})
            tag_objs.append(tag_obj)
        post.tags.set(tag_objs)
        return post
