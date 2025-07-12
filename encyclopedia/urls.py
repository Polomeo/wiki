from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("not_found/<str:entry>", views.entry_not_found, name="not-found"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.searchbar, name="search"),
]
