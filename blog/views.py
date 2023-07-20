from django.views.generic import ListView, DetailView
from .models import Post


class PostView(ListView):
    template_name = 'blog/post/list.html'
    model = Post
    context_object_name = 'posts'
    queryset = Post.published.all()


class PostDetailView(DetailView):
    template_name = 'blog/post/detail.html'
    model = Post
    context_object_name = 'post'

    def get_queryset(self):
        queryset = Post.published.all()
        return queryset
