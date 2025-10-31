# Update the title of the book
for book in books:
    if book.title == "1984":
        book.title = "Nineteen Eighty-Four"

# Display updated book
for book in books:
    print(f"Title: {book.title}, Author: {book.author}, Year: {book.year}")

# Expected Output:
# Title: Nineteen Eighty-Four, Author: George Orwell, Year: 1949
