from django.contrib import admin
from .models import Author, Category, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "sale_price", "is_recommended", "views", "created_at")
    list_filter = ("category", "author", "is_recommended", "book_format")
    search_fields = ("title", "author__name")
    prepopulated_fields = {"slug": ("title",)}
