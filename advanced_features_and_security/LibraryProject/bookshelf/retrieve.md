# Retrieve Operation for Book Model

```python
from bookshelf.models import Book  # Replace 'bookshelf' with your app name if different

# Retrieve a single book by title
book = Book.objects.get(title="1984")

# Display all attributes of the book
print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")

# Expected Output:
# Title: 1984, Author: George Orwell, Year: 1949
