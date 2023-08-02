from django.urls import path
from .views import PostView, post_share, post_comment, PostDetailView, \
    post_list, post_detail

urlpatterns = [
 # path('', PostView.as_view(), name='posts'),
 path('', post_list, name='posts'),
 path('<int:year>/<int:month>/<int:day>/<slug:post>/',
      post_detail, name='post'
      ),
 path('<int:post_id>/share/',
      post_share, name='post_share'),
 path('<int:post_id>/comment/', post_comment, name='post_comment'),
 path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag')
]

