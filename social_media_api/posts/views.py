from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generic, status
from .models import Like
from notifications.models import Notification
from django.shortcuts import get_object_or_404



class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        user = request.user

        # Check if post exists
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        # Prevent duplicate likes
        if Like.objects.filter(post=post, user=user).exists():
            return Response({"message": "You already liked this post"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the like
        Like.objects.create(post=post, user=user)

        # Create a notification for the post owner
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb="liked your post",
                target=post)

class ToggleLikeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # ↓ This is the missing line
        post = get_object_or_404(Post, pk=pk)

        # ↓ This is the second missing line
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            # User already liked → Unlike
            like.delete()
            return Response({"message": "Unliked"}, status=status.HTTP_200_OK)

        return Response({"message": "Liked"}, status=status.HTTP_201_CREATED)

class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        user = request.user

        # Check if post exists
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has liked the post
        like = Like.objects.filter(post=post, user=user).first()

        if not like:
            return Response({"message": "You have not liked this post"}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()

        return Response({"message": "Post unliked successfully"}, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()     # ✔ Required
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign logged-in user as author
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()   # ✔ Required
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign logged-in user as comment author
        serializer.save(author=self.request.user)
