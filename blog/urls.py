from django.urls import path
from .views import PostView, PostDetailView

urlpatterns = [
 path('', PostView.as_view(), name='posts'),
 path('<uuid:pk>', PostDetailView.as_view(), name='post'),
]
