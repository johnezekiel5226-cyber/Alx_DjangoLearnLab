# Create a Book instance
class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

books = []  # A simple list to store book instances

# Create the book
new_book = Book(title="1984", author="George Orwell", year=1949)
books.append(new_book)

# Expected Output:
# Book titled "1984" by George Orwell (1949) successfully created and added to the list.
print(f'Book titled "{new_book.title}" by {new_book.author} ({new_book.year}) successfully created.')
