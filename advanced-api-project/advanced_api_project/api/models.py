from rest_framework import serializers
from datetime import date
from .models import Author, Book

"""
Serializers for the Author and Book Models
------------------------------------------

1. BookSerializer:
   - Serializes all fields of the Book model.
   - Includes custom validation to prevent future publication years.

2. AuthorSerializer:
   - Serializes the author's name and ID.
   - Includes a nested BookSerializer to dynamically list all books
     related to the author.
   - This nested relationship works because of the 'related_name="books"'
     defined in the Book model. DRF automatically retrieves author.books.all()
     and passes the list into BookSerializer(many=True).

Together, these serializers provide clean representations of:
- An author and all their books (nested)
- A book with its associated author's ID
"""

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Includes:
    - Automatic serialization of all fields.
    - Custom validation to ensure publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        """
        Custom validator that ensures books cannot be published in the future.
        Runs automatically whenever publication_year is included in input data.
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. ({value} > {current_year})"
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes:
    - The author's ID and name.
    - A nested list of books written by the author (read-only).
      Uses BookSerializer to display each related book.

    The `books` field works because:
    - The Book model's ForeignKey includes related_name="books".
    - DRF automatically calls author.books.all() to populate this field.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
