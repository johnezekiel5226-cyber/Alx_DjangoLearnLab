from django.contrib import admin
from .models import Book  # ✅ Required import

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Show these fields in the list view
    list_display = ('title', 'author', 'publication_year')

    # Add filters for author and publication year
    list_filter = ('author', 'publication_year')

    # Enable searching by title or author
    search_fields = ('title', 'author')
