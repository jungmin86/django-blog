from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/<int:id>/", views.post_detail, name="post_detail"),
    path("post/new", views.post_new, name="post_new"),
    path("post/<int:id>/edit/", views.post_edit, name="post_edit"),
    path(r"^drafts/$", views.post_draft_list, name="post_draft_list"),
    path(r"^post/(?P<id>\d+)/publish/$", views.post_publish, name="post_publish"),
    path(r"^post/(?P<id>\d+)/remove/$", views.post_remove, name="post_remove"),
]
