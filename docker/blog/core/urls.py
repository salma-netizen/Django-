from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import *

urlpatterns = [
    path('', welcome, name='welcome'),
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('editprofile', editprofile,name='editprofile'),
    path("posts", post, name="post"),
    path('subscribe/<cat_id>', subscribe, name="subscribe"),
    path('unsubscribe/<cat_id>', unsubscribe, name="unsubscribe"),
    path('cat-posts/<cat_id>', catPosts, name='cat-posts'),
    path("<int:pk>", PostDetailView.as_view(), name="details"),
    path("create", createpost, name="createpost"),
    path("delete/<int:pk>", PostDelete.as_view(), name="deletepost"),
    path("edit/<post_id>", editpost, name="editpost"),
    path('<int:pk>/like', AddLike.as_view(), name='like'),
    path('<int:pk>/dislike', AddDislike.as_view(), name='dislike'),
    path('post/<int:post_pk>/comment/<int:pk>/like', AddCommentLike.as_view(), name='comment-like'),
    path('post/<int:post_pk>/comment/<int:pk>/dislike', AddCommentDislike.as_view(), name='comment-dislike'),
    path("comment/<int:pk>", CommentDeleteView.as_view(), name="deletecomment"),
    path('post/<int:post_pk>/comment/<int:pk>/reply', CommentReplyView.as_view(), name='comment-reply'),
    path('search/', search, name="search"),
    path('tag/<slug:slug>/', tagged, name="tagged"),


]