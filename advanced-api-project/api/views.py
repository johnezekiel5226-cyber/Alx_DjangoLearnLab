# api/views.py
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Book
from .serializers import BookSerializer


# -----------------------------
# 1. LIST VIEW (small change)
# Added: simple filtering using get_queryset()
# -----------------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    # ADDED: Filtering by author
    def get_queryset(self):
        queryset = super().get_queryset()
        author = self.request.query_params.get("author")
        if author:
            queryset = queryset.filter(author__icontains=author)
        return queryset


# -----------------------------
# 2. DETAIL VIEW (unchanged)
# -----------------------------
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny] 

# -----------------------------
# 3. CREATE VIEW (CHANGED)
# ADDED:
# - permission_classes
# - custom validation for title uniqueness
# - perform_create override
# -----------------------------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # ADDED: Only authenticated users can create
    permission_classes = [permissions.IsAuthenticated]

    # ADDED: Custom validation before creating a book
    def perform_create(self, serializer):
        title = self.request.data.get("title")

        # Prevent duplicate titles
        if Book.objects.filter(title__iexact=title).exists():
            raise ValidationError({"title": "A book with this title already exists."})

        serializer.save()


# -----------------------------
# 4. UPDATE VIEW (CHANGED)
# ADDED:
# - permission_classes
# - custom validation (title cannot be empty)
# - perform_update override
# -----------------------------
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # ADDED: Only authenticated users can update
    permission_classes = [permissions.IsAuthenticated]

    # ADDED: Custom update logic
    def perform_update(self, serializer):
        title = self.request.data.get("title")
        if title == "":
            raise ValidationError({"title": "Title cannot be empty."})

        serializer.save()


# -----------------------------
# 5. DELETE VIEW (CHANGED)
# ADDED: Only admin can delete
# -----------------------------
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # ADDED: Only admins can delete books
    permission_classes = [permissions.IsAdminUser]
