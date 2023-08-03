from django import template
from django.db.models import Count, QuerySet
from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count: int = 5) -> dict[str, QuerySet[Post]]:
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count: int = 5) -> QuerySet[Post]:
    """
    У наведеному шаблонному тезі за допомогою функції annotate() формується
    набір запитів QuerySet, щоб агрегувати загальну кількість коментарів до
    кожного поста. Функція агрегування Count використовується для
    збереження кількості коментарів у обчислюваному полі total_comments за
    кожному об'єкту Post. Набір запитів QuerySet упорядковується
    за обчислюваним полем у спадному порядку. Також надається опціональна
    змінна count, щоб обмежувати загальну кількість об'єктів, що повертаються.
    :param count: Count of comments
    :return: QuerySet[Post]
    """
    return Post.published.annotate(total_comments=Count('comments')) \
               .order_by('-total_comments')[:count]
