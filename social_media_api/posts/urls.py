from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from .views import UserFeedView
from .views import UserListView
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
from .views import LikePostView, UnlikePostView


urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserListView.as_view(), name='user_list'),
    path('feed/', UserFeedView.as_view(), name='user_feed'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like_post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike_post'),
]
