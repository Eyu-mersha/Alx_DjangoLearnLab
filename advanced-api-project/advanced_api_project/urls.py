"""
URL configuration for advanced_api_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import ListView, DetailView, CreateView, UpdateView, DeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', ListView.as_view(), name='book-list'),  # List all books and create a new one
    path('books/<int:pk>/', DetailView.as_view(), name='book-detail'),  # Get a single book by ID
    path('books/create/', CreateView.as_view(), name='book-create'),  # Create a new book
    path('books/<int:pk>/update/', UpdateView.as_view(), name='book-update'),  # Update an existing book
    path('books/<int:pk>/delete/', DeleteView.as_view(), name='book-delete'),  # Delete a book
]
