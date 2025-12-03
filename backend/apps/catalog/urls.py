from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("kategoriya/<slug:slug>/", views.category_detail, name="category_detail"),
    path("kitob/<int:id>/<slug:slug>/", views.book_detail, name="book_detail"),
    path("qidiruv/", views.search, name="search"),
    path("sevimlilar/", views.favorites, name="favorites"),
]
