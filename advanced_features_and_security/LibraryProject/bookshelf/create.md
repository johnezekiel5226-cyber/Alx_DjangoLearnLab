# Create Operation for Book Model

```python
from bookshelf.models import Book  # Replace 'bookshelf' with your app name if different

# Create a new Book instance in the database
new_book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Display the created book
print(new_book)

# Expected Output:
# <Book: 1984 by George Orwell (1949)>
