from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404

@permission_required('bookshelf.add_book', raise_exception=True)
def create_book(request):
    if request.method == "POST":
        # handle form submission
        ...
    return render(request, 'bookshelf/create_book.html')

query = request.GET.get("q", "")
books = Book.objects.filter(title__icontains=query)

@permission_required('bookshelf.change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    pass

    if request.method == "POST":
        # update logic
        ...

    return render(request, 'bookshelf/edit_book.html', {'book': book})

@permission_required('bookshelf.delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_list')

@permission_required('bookshelf.view_book', raise_exception=True)
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data["q"]
        results = Book.objects.filter(title__icontains=query)
    else:
        results = Book.objects.none()

    return render(request, "bookshelf/search.html", {"form": form, "results": results})

response = render(request, "bookshelf/index.html")
response["Content-Security-Policy"] = "default-src 'self'"
return response
