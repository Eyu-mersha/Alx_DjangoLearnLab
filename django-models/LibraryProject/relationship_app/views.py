# Create your views here.
from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
# relationship_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden
from .models import Book
from .forms import BookForm
  # Assume you have a form for creating/updating books
# relationship_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm

# View to add a new book
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to the book list page
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})

# View to edit an existing book
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to the book list page
    else:
        form = BookForm(instance=book)

    return render(request, 'edit_book.html', {'form': form, 'book': book})

# View to delete a book
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  # Redirect after deletion

    return render(request, 'delete_book.html', {'book': book})

# relationship_app/views.py
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

# Check for Admin role
def Admin(user):
    return user.userprofile.role == 'Admin'

# Check for Librarian role
def is_librarian(user):
    return user.userprofile.role == 'Librarian'

# Check for Member role
def is_member(user):
    return user.userprofile.role == 'Member'

# Admin view
@user_passes_test(is_admin)
def Admin(request):
    return HttpResponse("Welcome, Admin! You have access to this page.")

# Librarian view
@user_passes_test(is_librarian)
def librarian_view(request):
    return HttpResponse("Welcome, Librarian! You have access to this page.")

# Member view
@user_passes_test(is_member)
def member_view(request):
    return HttpResponse("Welcome, Member! You have access to this page.")


# User registration view using Django's built-in UserCreationForm
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # After successful registration, log the user in
            username = form.cleaned_data.get('username')
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('home')  # Redirect to a home page (change as needed)
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})




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
