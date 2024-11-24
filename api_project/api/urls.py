# api/urls.py
from django.urls import path
from .views import BookList

# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token  # Import the token retrieval view

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('', include(router.urls)),  # Include all the routes registered with the router
    path('books/', BookList.as_view(), name='book-list'),
     path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # Other routes (like your BookViewSet) will follow here
]
# api/urls.py

