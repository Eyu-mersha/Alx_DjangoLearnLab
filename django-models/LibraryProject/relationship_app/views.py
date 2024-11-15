# Create your views here.
from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView


# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()  # Get all books from the database
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view to display library details and its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # Template to render library details
    context_object_name = 'library'  # This will be used in the template

    # Optionally, you can override the get_context_data method to add extra context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adding extra context for books in the library
        context['books'] = self.object.books.all()  # Get books associated with the library
        return context
