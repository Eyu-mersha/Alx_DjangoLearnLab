from django.urls import path
from .views import list_books
from . import views

urlpatterns = [
    path('books/', views.list_books, name='list_books'),  # Route to the function-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # Route to the class-based view
]
