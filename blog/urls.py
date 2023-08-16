from django.urls import path

from .feeds import LatestPostsFeed
from .views import post_share, post_comment, \
    post_list, post_detail, post_search

urlpatterns = [
 path('', post_list, name='posts'),
 path('<int:year>/<int:month>/<int:day>/<slug:post>/',
      post_detail, name='post'
      ),
 path('<int:post_id>/share/',
      post_share, name='post_share'),
 path('<int:post_id>/comment/', post_comment, name='post_comment'),
 path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
 path('feed/', LatestPostsFeed(), name='post_feed'),
 path('search/', post_search, name='post_search')
]
