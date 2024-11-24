from django.shortcuts import render
from rest_framework import generics
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
