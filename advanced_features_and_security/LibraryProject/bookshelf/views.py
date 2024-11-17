from django.shortcuts import render
# bookshelf/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book

# View for listing books (viewing)
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

# View for creating a new book (creating)
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        published_date = request.POST.get('published_date')
        Book.objects.create(
            title=title, 
            author=author, 
            description=description, 
            published_date=published_date
        )
        return redirect('book_list')
    return render(request, 'bookshelf/create_book.html')

# View for editing a book (editing)
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.description = request.POST.get('description')
        book.published_date = request.POST.get('published_date')
        book.save()
        return redirect('book_list')
    return render(request, 'bookshelf/edit_book.html', {'book': book})

# View for deleting a book (deleting)
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_list')

# Create your views here.
