from django.urls import path
from .views import list_books
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # User authentication URLs
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout view
    path('register/', views.register, name='register'),  # Registration view
    # Other app URLs can be added here
    path('books/', views.list_books, name='list_books'),  # Route to the function-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # Route to the class-based view

]


