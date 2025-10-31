# Delete Operation for Book Model

```python
from bookshelf.models import Book  # Required import

# Retrieve the book to delete
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book from the database
book.delete()

# Confirm deletion
books = Book.objects.all()
if not books:
    print("No books found. Deletion successful.")
else:
    for b in books:
        print(f"Title: {b.title}, Author: {b.author}, Year: {b.publication_year}")

# Expected Output:
# No books found. Deletion successful.
