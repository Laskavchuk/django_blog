import faker
import pytest
import factory
from django.contrib.auth.models import User
from django.db import connection
from pytest_factoryboy import register

from blog.models import Post
from project.model_choices import Status

fake = faker.Faker()

@pytest.fixture(autouse=True)
def enable_pg_trgm_for_tests():
    with connection.cursor() as cursor:
        cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')

@pytest.fixture(scope='session')
def faker_fixture():
    yield fake


@pytest.fixture(autouse=True)
def django_db_setup(db):
    yield
@register
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.LazyAttribute(lambda x: fake.word())
    password = factory.Faker('password')  # Генерує фейковий пароль

    class Meta:
        model = User
@register
class PostFactory(factory.django.DjangoModelFactory):
    title = factory.LazyAttribute(lambda x: fake.word())
    slug = factory.LazyAttribute(lambda x: fake.slug())
    author = factory.SubFactory(UserFactory)
    body = (lambda x: fake.sentences())
    status = Status.PUBLISHED

    class Meta:
        model = Post


