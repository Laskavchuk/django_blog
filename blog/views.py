from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag
from django.db.models import Count

from project.model_choices import Status
from .forms import EmailPostForm, SearchForm
from .model_forms import CommentForm
from .models import Post

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .tasks import send_email_task


class PostView(ListView):
    template_name = 'blog/post/list.html'
    context_object_name = 'posts'
    queryset = Post.published.all()
    paginate_by = 3

    # def get_queryset(self):
    #     tag_slug = None
    #     if tag_slug:
    #         tag = get_object_or_404(Tag, slug=tag_slug)
    #         return Post.published.filter(tags__in=[tag])
    #     return super().get_queryset()


# class PostDetailView(DetailView):
#     template_name = 'blog/post/detail.html'
#     context_object_name = 'post'
#     slug_url_kwarg = 'post'
#     queryset = Post.published.all()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['comments'] = self.object.comments.filter(active=True)
#         context['form'] = CommentForm()
#         return context


def post_share(request, post_id):
    # Извлечь пост по его идентификатору id
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            send_email_task.delay(post_id, cd)
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Status.PUBLISHED)
    comment = None
    # Коментар був надісланий
    form = CommentForm(request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post,
                                                      'form': form,
                                                      'comment': comment})


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    # Список схожих постов
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]
    context = {'post': post,
               'comments': comments,
               'form': form,
               'similar_posts': similar_posts}
    return render(request,
                  'blog/post/detail.html', context)


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # search_vector = SearchVector('title', weight='A') + \
            #                 SearchVector('body', weight='B')
            # search_query = SearchQuery(query, config='spanish')
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')
    context = {'form': form,
               'query': query,
               'results': results}
    return render(request, 'blog/post/search.html', context)
