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
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

# Check for Admin role
def is_admin(user):
    return user.userprofile.role == 'Admin'

# Check for Librarian role
def is_librarian(user):
    return user.userprofile.role == 'Librarian'

# Check for Member role
def is_member(user):
    return user.userprofile.role == 'Member'

# Admin view
@user_passes_test(is_admin)
def admin_view(request):
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
