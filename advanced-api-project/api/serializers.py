from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):

     def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value and value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

     class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_year', 'created_at']
