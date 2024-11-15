import django
import os

# Set up Django settings for script execution
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")  # Replace with your actual project name
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    print(f"Books by {author.name}:")
    for book in books:
        print(f"- {book.title}")

# 2. List all books in a specific library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()  # Many-to-Many relationship
    print(f"Books in {library.name}:")
    for book in books:
        print(f"- {book.title}")

# 3. Retrieve the librarian for a library
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library)  # One-to-One relationship
    print(f"The librarian for {library.name} is {librarian.name}")

# Example usage
if __name__ == "__main__":
    # Replace with real data in your database
    books_by_author("George Orwell")
    books_in_library("Central Library")
    librarian_for_library("Central Library")
