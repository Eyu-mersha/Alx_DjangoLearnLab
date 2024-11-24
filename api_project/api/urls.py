# api/urls.py
from django.urls import path
from .views import BookList

# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('', include(router.urls)),  # Include all the routes registered with the router
    path('books/', BookList.as_view(), name='book-list'),
]
