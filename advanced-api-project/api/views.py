from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework
import django_filters

# Create a custom filter class
class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title')
    author = django_filters.CharFilter(lookup_expr='icontains', label='Author')
    publication_year = django_filters.NumberFilter(lookup_expr='exact', label='Publication Year')

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

class ListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = BookFilter
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering by title
    permission_classes = []  # No authentication required for the list view

# Retrieve a single book
class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []  # Allow unauthenticated users to view the book

# Create a new book
class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Restrict to authenticated users

# Update an existing book
class UpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Restrict to authenticated users

# Delete a book
class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Restrict to authenticated users

