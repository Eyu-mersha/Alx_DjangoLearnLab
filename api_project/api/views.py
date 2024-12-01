from django.shortcuts import render
from rest_framework import generics

from advanced_api_project.api import serializers
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()  # Get all books from the database
    serializer_class = BookSerializer  # Use the BookSerializer to serialize the data
# api/views.py

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # All users must be authenticated to view or modify books

    def get_permissions(self):
        if self.action == 'destroy':  # Only admins can delete books
            return [IsAdminUser()]
        return super().get_permissions()  # Default to IsAuthenticated for other actions
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated

# List all books
class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []  # Allow unauthenticated users to view the list

# Retrieve a single book
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []  # Allow unauthenticated users to view the book

# Create a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        publication_year = serializer.validated_data.get('publication_year')
        if publication_year > 2024:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        serializer.save()

# Update an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        publication_year = serializer.validated_data.get('publication_year')
        if publication_year > 2024:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        serializer.save()
  # Restrict to authenticated users

# Delete a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Restrict to authenticated users
