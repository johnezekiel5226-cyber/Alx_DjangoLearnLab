# Delete the book
books = [book for book in books if book.title != "Nineteen Eighty-Four"]

# Try to retrieve all books
if not books:
    print("No books found. Deletion successful.")
else:
    for book in books:
        print(f"Title: {book.title}, Author: {book.author}, Year: {book.year}")

# Expected Output:
# No books found. Deletion successful.
