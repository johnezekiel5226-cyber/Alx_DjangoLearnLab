from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Post

class PostForm(forms.ModelForm):
class Meta:
model = Post
fields = ['title', 'content']
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
