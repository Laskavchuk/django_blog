from django.urls import path
from .views import PostView, post_detail, post_share, post_comment

urlpatterns = [
 path('', PostView.as_view(), name='posts'),
 path('<int:year>/<int:month>/<int:day>/<slug:post>/',
      post_detail, name='post'
      ),
 path('<uuid:post_id>/share/',
      post_share, name='post_share'),
 path('<uuid:post_id>/comment/', post_comment, name='post_comment'),
]

