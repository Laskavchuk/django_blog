from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from model_choices import Status
from .models import Post
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PostView(ListView):
    template_name = 'blog/post/list.html'
    context_object_name = 'posts'
    queryset = Post.published.all()
    paginate_by = 3


# def post_list(request):
#     post_list = Post.published.all()
#     # Постраничная разбивка с 3 постами на страницу
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         # Если page_number не целое число, то
#         # выдать первую страницу
#         posts = paginator.page(1)
#     except EmptyPage:
#         # Если page_number находится вне диапазона, то
#         # выдать последнюю страницу
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                   'blog/post/list.html',
#                   {'posts': posts})


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/post/detail.html'
#     context_object_name = 'post'
#     slug_url_kwarg = 'post'
#     queryset = Post.objects.filter(status=Status.PUBLISHED)
#
#     def get_object(self, queryset=None):
#         year = self.kwargs.get('year')
#         month = self.kwargs.get('month')
#         day = self.kwargs.get('day')
#         post_slug = self.kwargs.get('post')
#
#         return get_object_or_404(
#             Post,
#             status=Status.PUBLISHED,
#             slug=post_slug,
#             publish__year=year,
#             publish__month=month,
#             publish__day=day
#         )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
