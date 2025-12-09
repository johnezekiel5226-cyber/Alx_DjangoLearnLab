from django.urls import path
from .views import LikePostView, UnlikePostView
PostViewSet,CommentViewSet,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns += router.urls


urlpatterns = [
    path('<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:post_id>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]
