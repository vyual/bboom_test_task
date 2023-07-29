from django.urls import path

from .views import *

urlpatterns = [
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:user_id>/posts/', UserPostsListView.as_view(), name='user-posts-list'),
    path('api/posts/', PostCreateView.as_view(), name='post-create'),
    path('api/posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('users/', user_list, name='user-list'),
    path('users/<int:user_id>/', user_posts_list, name='user-posts-list'),
    path('post/create/', post_create, name='post-create'),
    path('post/delete/<int:post_id>/',post_delete, name='post-delete'),
]
