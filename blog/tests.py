from django.contrib.auth.models import User
from django.urls import reverse

from blog.models import Post
from model_choices import Status


def test_posts(client, faker):
    url = reverse('posts')
    response = client.get(url)
    assert response.status_code == 200

    assert len(response.context['posts']) == Post.objects.count()

    for _ in range(2):
        Post.objects.create(
            title=faker.word(),
            slug=faker.slug(),
            author=User.objects.create_user(username=faker.word(),
                                            password=faker.password()),
            body=faker.sentences(),
            status=Status.PUBLISHED
        )

    url = reverse('posts')
    response = client.get(url)
    assert response.status_code == 200
    assert len((response.context['posts'])) == Post.objects.count()

    Post.objects.create(
        title=faker.word(),
        slug=faker.slug(),
        author=User.objects.create_user(username=faker.word(),
                                        password=faker.password()),
        body=faker.sentences(),
        status=Status.DRAFT
    )

    url = reverse('posts')
    response = client.get(url)
    assert response.status_code == 200
    assert not len((response.context['posts'])) == Post.objects.count()
