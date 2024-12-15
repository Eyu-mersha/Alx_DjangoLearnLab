from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from .views import UserFeedView
from .views import UserListView
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserListView.as_view(), name='user_list'),
    path('feed/', UserFeedView.as_view(), name='user_feed'),
]
