from django.urls import path
from .views import LikePostView, UnlikePostView

urlpatterns = [
    path('<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:post_id>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]
