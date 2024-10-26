from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.serach, name="search"),
    path("new", views.new_page, name="new_page"),
    path("edit/<str:title>", views.edit_page, name="edit_page"),
    path("random", views.random_page, name="random_page")
]
