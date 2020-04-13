from django.contrib import admin

from .models import Post, Poster

class PostInline(admin.StackedInline):
    model = Post
    extra = 1

class PosterAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Poster information', {'fields': ['user', 'poster_name', 'poster_handle', 'poster_pfp', 'poster_password', 'liked_posts']}),
    ]
    inlines = [PostInline]

admin.site.register(Poster, PosterAdmin)
admin.site.register(Post)
