# api/tests/factories.py
import factory
from api.models import Book

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = "Sample Book"
    author = "John Doe"
