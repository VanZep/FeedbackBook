from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Genre, Title, Review, Comment, CustomUser


UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('bio', 'role', 'confirmation_code')}),)
UserAdmin.list_display = ('username', 'role', 'email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    list_display_links = ('name', )
    list_per_page = 10
    readonly_fields = ['name', 'slug']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    list_display_links = ('name', )
    list_per_page = 10
    readonly_fields = ['name', 'slug']


class GenreListAdmin(admin.StackedInline):
    fields = ['name', 'slug']
    list_display = ('get_title', )

    @admin.display(description='title')
    def get_title(self, obj):
        return [title.name for title in obj.title.all()]


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category', 'get_genre')
    search_fields = ('name', 'year', 'category', 'genre')
    list_filter = ('name', 'year', 'category', 'genre')
    list_display_links = ('name', )
    list_per_page = 10

    @admin.display(description='genre')
    def get_genre(self, obj):
        return [genre.name for genre in obj.genre.all()]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'score')
    search_fields = ('title', 'author', 'score')
    list_filter = ('title', 'author', 'score')
    list_display_links = ('title', 'author')
    list_per_page = 10
    readonly_fields = ['title', 'author']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author')
    search_fields = ('review', 'author')
    list_filter = ('review', 'author')
    list_display_links = ('review', 'author')
    list_per_page = 10
    readonly_fields = ['review', 'author']


admin.site.register(CustomUser, UserAdmin)
