from django.urls import path
from .views import list_books
from . import views
from django.contrib.auth import views as auth_views
# relationship_app/urls.py
from django.urls import path


urlpatterns = [
    # User authentication URLs
        path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register')
    # Other app URLs can be added here
    path('books/', views.list_books, name='list_books'),  # Route to the function-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # Route to the class-based view

]
