from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Book, Author


def home(request):
    categories = Category.objects.all()
    best_selling = Book.objects.order_by("-views")[:6]
    new_books = Book.objects.order_by("-created_at")[:6]
    recommended = Book.objects.filter(is_recommended=True).order_by("-created_at")[:6]
    return render(
        request,
        "home.html",
        {
            "categories": categories,
            "best_selling": best_selling,
            "new_books": new_books,
            "recommended": recommended,
        },
    )


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(category=category)
    authors = Author.objects.filter(books__category=category).distinct()

    author_id = request.GET.get("author")
    if author_id:
        books = books.filter(author_id=author_id)

    sort = request.GET.get("sort")
    sort_map = {
        "price_asc": "sale_price",
        "price_desc": "-sale_price",
        "newest": "-created_at",
        "oldest": "created_at",
        "popular": "-views",
    }
    if sort in sort_map:
        books = books.order_by(sort_map[sort])

    return render(
        request,
        "category_list.html",
        {
            "category": category,
            "books": books,
            "authors": authors,
            "current_author": author_id,
            "current_sort": sort,
        },
    )


def book_detail(request, id, slug):
    book = get_object_or_404(Book, id=id, slug=slug)
    Book.objects.filter(id=book.id).update(views=book.views + 1)
    return render(request, "book_detail.html", {"book": book})


def search(request):
    query = request.GET.get("q", "").strip()
    books = Book.objects.none()
    authors = Author.objects.none()
    author_id = request.GET.get("author")
    sort = request.GET.get("sort")
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query)
            | Q(author__name__icontains=query)
            | Q(category__name__icontains=query)
        ).select_related("author", "category")
        if author_id:
            books = books.filter(author_id=author_id)
        sort_map = {
            "price_asc": "sale_price",
            "price_desc": "-sale_price",
            "newest": "-created_at",
            "oldest": "created_at",
            "popular": "-views",
        }
        if sort in sort_map:
            books = books.order_by(sort_map[sort])
        authors = Author.objects.filter(books__in=books).distinct()
    return render(
        request,
        "search_results.html",
        {
            "query": query,
            "books": books,
            "authors": authors,
            "current_author": author_id,
            "current_sort": sort,
        },
    )
