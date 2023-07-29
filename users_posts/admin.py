from django.contrib import admin

from users_posts.models import Post


@admin.register(Post)
class Post(admin.ModelAdmin):
    list_display = [
        'user',
        'title',
        'body',
    ]
