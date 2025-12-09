from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # unread first
        notifications = Notification.objects.filter(recipient=user).order_by('read', '-timestamp')

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        user = request.user

        try:
            notification = Notification.objects.get(id=notification_id, recipient=user)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=404)

        notification.read = True
        notification.save()

        return Response({"message": "Notification marked as read"})

class MarkAllNotificationsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        Notification.objects.filter(recipient=user, read=False).update(read=True)

        return Response({"message": "All notifications marked as read"})
