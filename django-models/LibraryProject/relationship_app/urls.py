from django.urls import path
from .views import list_books
from . import views
from django.contrib.auth import views as auth_views
# relationship_app/urls.py
from django.urls import path
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # User authentication URLs
    # URL pattern for adding a new book
    path('add_book/', views.add_book, name='add_book'),  
    
    # URL pattern for editing a book
    path('edit_book/', views.edit_book, name='edit_book'),  
    
    # URL pattern for deleting a book
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('admin/', admin.site.urls),
    path('books/', include('relationship_app.urls')),
    path('admin/', views.admin_view, name='Admin'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    # Other app URLs can be added here
    path('books/', views.list_books, name='list_books'),  # Route to the function-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # Route to the class-based view

]
