import requests
import factory

from .. import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from faker import Faker
fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda o: fake.unique.user_name())
    password = factory.PostGenerationMethodCall('set_password', 'pass')
    email = factory.LazyAttribute(lambda o: fake.unique.email())
    first_name = factory.LazyAttribute(lambda o: fake.first_name())
    last_name = factory.LazyAttribute(lambda o: fake.last_name())


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UserProfile
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
    slug = factory.LazyAttribute(lambda o: slugify(o.user.username))
    profile_image = factory.LazyAttribute(
        lambda o: generate_profile_image(o.user.first_name + '+' + o.user.last_name))
    description = factory.LazyAttribute(lambda o: fake.text())
    date_created = factory.LazyAttribute(lambda o: fake.date_time())


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tag

    name = factory.LazyAttribute(lambda o: fake.unique.word())
    slug = factory.LazyAttribute(lambda o: fake.unique.slug())


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Post

    user_profile = factory.Iterator(models.UserProfile.objects.all())
    title = factory.LazyAttribute(lambda o: fake.unique.sentence())
    slug = factory.LazyAttribute(lambda o: fake.slug())
    featured_image = factory.LazyAttribute(
        lambda o: generate_post_featured_image())
    content = factory.LazyAttribute(lambda o: fake.paragraph(nb_sentences=120))
    excerpt = factory.LazyAttribute(lambda o: fake.text())

# https://ui-avatars.com/api/?name=John+Doe&background=random&bold=true&uppercase=true&format=svg
def generate_profile_image(_full_name):
    response = requests.get('https://ui-avatars.com/api', params={
        'name': _full_name,
        'uppercase': 'true',
        'bold': 'true',
        'background': '#d8fc82',
        'color': '#0f1825',
        'format': 'svg',
    })
    response.raise_for_status()
    return response.url

# https://random.imagecdn.app/1400/600
def generate_post_featured_image():
    response = requests.get('https://random.imagecdn.app/1400/600')
    response.raise_for_status()
    return response.url
