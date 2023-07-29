from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from .forms import PostForm
from .models import Post
from .serializers import UserSerializer, PostSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication]


class UserPostsListView(generics.ListAPIView):
    serializer_class = PostSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Post.objects.filter(user__id=int(user_id))


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    authentication_classes = [SessionAuthentication]


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [SessionAuthentication]


# Представление для отображения списка всех пользователей
def user_list(request):
    users = User.objects.all()
    return render(request, 'users_posts/user_list.html', {'users': users})


# Представление для отображения списка постов конкретного пользователя
def user_posts_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user)
    return render(request, 'users_posts/user_posts_list.html', {'user': user, 'posts': posts})


# Представление для добавления нового поста
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('user-posts-list', user_id=request.user.id)
    else:
        form = PostForm()
    return render(request, 'users_posts/post_create.html', {'form': form})


# Представление для удаления поста
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
        return JsonResponse({'message': 'Пост успешно удален.'})
    else:
        return JsonResponse({'message': 'У вас нет прав на удаление этого поста.'})
