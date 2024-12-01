# api/urls.py
from django.urls import path, include
from .views import BookList
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token  # Import the token retrieval view
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('', include(router.urls)),  # Include all the routes registered with the router
    path('books/', BookList.as_view(), name='book-list'),
     path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
        path('books/', BookListView.as_view(), name='book-list'),  # List all books and create a new one
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # Get a single book by ID
    path('books/create/', BookCreateView.as_view(), name='book-create'),  # Create a new book
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),  # Update an existing book
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),  # Delete a book
    # Other routes (like your BookViewSet) will follow here
]
