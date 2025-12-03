from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Book, Author, Banner


def home(request):
    categories = Category.objects.all()
    banners = Banner.objects.filter(is_active=True).order_by("order", "-created_at")[:5]
    best_selling = Book.objects.order_by("-views")[:6]
    new_books = Book.objects.order_by("-created_at")[:6]
    recommended = Book.objects.filter(is_recommended=True).order_by("-created_at")[:6]
    return render(
        request,
        "home.html",
        {
            "categories": categories,
            "banners": banners,
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
    categories = Category.objects.all()
    author_id = request.GET.get("author")
    category_slug = request.GET.get("category")
    sort = request.GET.get("sort")
    limit = request.GET.get("limit")
    sort_options = [
        ("", "Mosligi bo‘yicha"),
        ("popular", "Eng saralar"),
        ("newest", "Yangi"),
        ("alpha_asc", "Alifbo (A-Z)"),
        ("alpha_desc", "Alifbo (Z-A)"),
        ("price_desc", "Narx (qimmat-arzon)"),
        ("price_asc", "Narx (arzon-qimmat)"),
    ]
    limit_options = ["8", "12", "16", "24", "32"]
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query)
            | Q(author__name__icontains=query)
            | Q(category__name__icontains=query)
        ).select_related("author", "category")
        if author_id:
            books = books.filter(author_id=author_id)
        if category_slug:
            books = books.filter(category__slug=category_slug)
        sort_map = {
            "price_asc": "sale_price",
            "price_desc": "-sale_price",
            "newest": "-created_at",
            "oldest": "created_at",
            "popular": "-views",
            "alpha_asc": "title",
            "alpha_desc": "-title",
        }
        if sort in sort_map:
            books = books.order_by(sort_map[sort])
        authors = Author.objects.filter(books__in=books).distinct()
        if limit:
            try:
                limit_int = int(limit)
                if limit_int > 0:
                    books = books[:limit_int]
            except ValueError:
                pass
    return render(
        request,
        "search_results.html",
        {
            "query": query,
            "books": books,
            "authors": authors,
            "current_author": author_id,
            "current_sort": sort,
            "categories": categories,
            "current_category": category_slug,
            "current_limit": limit,
            "sort_options": sort_options,
            "limit_options": limit_options,
        },
    )


def favorites(request):
    # Placeholder view for favorites list
    return render(request, "favorites.html")
