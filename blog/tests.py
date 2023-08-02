from django.contrib.auth.models import User
from django.urls import reverse

from blog.models import Post
from model_choices import Status


def test_posts(client, faker):
    url = reverse('posts')
    response = client.get(url)
    assert response.status_code == 200

    assert len(response.context['posts']) == Post.objects.count()
    date = faker.date()
    year = date[:4]
    month = date[5:-3]
    day = date[8:]
    slug = faker.slug()

    response = client.get(reverse('post', args=(year, day, month, slug,)))
    assert response.status_code == 404
    post = Post.objects.create(
            title=faker.word(),
            slug=faker.slug(),
            author=User.objects.create_user(username=faker.word(),
                                            password=faker.password()),
            body=faker.sentences(),
            status=Status.PUBLISHED
        )
    for _ in range(2):
        Post.objects.create(
            title=faker.word(),
            slug=faker.slug(),
            author=User.objects.create_user(username=faker.word(),
                                            password=faker.password()),
            body=faker.sentences(),
            status=Status.PUBLISHED
        )
    response = client.get(reverse('post', args=(post.created.year,
                                                post.created.month,
                                                post.created.day,
                                                post.slug
                                                )))
    assert response.status_code == 200

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


def test_post_share(client, faker):
    post = Post.objects.create(
        title=faker.word(),
        slug=faker.slug(),
        author=User.objects.create_user(username=faker.word(),
                                        password=faker.password()),
        body=faker.sentences(),
        status=Status.PUBLISHED
    )
    url = reverse('post_share', args=[post.id])
    response = client.get(url)
    assert response.status_code == 200

    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert all(v == ['This field is required.']
               for v in response.context['form'].errors.values())

    data = {
        'name': faker.name(),
        'email': faker.email(),
        'to': faker.email()
    }
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200


def test_comment_post(client, faker):
    post = Post.objects.create(
        title=faker.word(),
        slug=faker.slug(),
        author=User.objects.create_user(username=faker.word(),
                                        password=faker.password()),
        body=faker.sentences(),
        status=Status.PUBLISHED
    )
    url = reverse('post_comment', args=[post.id])
    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert all(v == ['This field is required.']
               for v in response.context['form'].errors.values())
    data = {
        'name': faker.name(),
        'email': faker.email(),
        'body': faker.sentence()
    }
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
