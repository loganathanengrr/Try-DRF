from django.urls import path

from .views import BlogPostRUDView, BlogPostAPIView

app_name = 'postings'

urlpatterns = [
    path('postings/<int:id>/', BlogPostRUDView.as_view(), name="post-rud"),
    path('postings/', BlogPostAPIView.as_view(), name="post-listcreate"),
]
