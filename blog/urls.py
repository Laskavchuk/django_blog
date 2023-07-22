from django.urls import path
from .views import PostView, post_detail

urlpatterns = [
 path('', PostView.as_view(), name='posts'),
 path('<int:year>/<int:month>/<int:day>/<slug:post>/',
      post_detail, name='post'
      ),
]
