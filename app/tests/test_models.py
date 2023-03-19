from django.test import TestCase
from django.contrib.auth.models import User
from app.models import *


class UserProfileCase(TestCase):

    def create_user_profile(self, first_name, last_name, username, email, password, profile_image, profile_description):
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )

        user_profile = user.profile
        user_profile.profile_image = profile_image
        user_profile.description = profile_description

        return user, user_profile


class TagCase(TestCase):

    def create_tag(self, name):
        tag = Tag.objects.create(name=name)
        return tag

    def create_tags(self, tag_names):
        tags = []

        for tag_name in tag_names:
            tag = Tag(name=tag_name)
            tags.append(tag)

        tags = Tag.objects.bulk_create(tags)
        return tags


class TestUserProfileModel(UserProfileCase):

    def setUp(self):
        self.user1, self.user_profile1 = self.create_user_profile(
            'John',
            'Doe',
            'johndoe',
            'johndoe@example.com',
            'password123',
            'https://example.com/api/image',
            'Some description'
        )

    def test_user_creation(self):
        self.assertIsInstance(self.user1, User)
        self.assertEqual(self.user1.first_name, 'John')
        self.assertEqual(self.user1.last_name, 'Doe')
        self.assertEqual(self.user1.username, 'johndoe')
        self.assertEqual(self.user1.email, 'johndoe@example.com')
        self.assertTrue(self.user1.check_password('password123'))

    def test_user_profile_creation(self):
        self.assertIsInstance(self.user_profile1, UserProfile)
        self.assertEqual(self.user_profile1.user, self.user1)
        self.assertEqual(self.user_profile1.slug, 'johndoe')
        self.assertEqual(self.user_profile1.profile_image,
                         'https://example.com/api/image')
        self.assertEqual(self.user_profile1.description, 'Some description')
        self.assertIn(self.user_profile1, self.user_profile1.following.all())
        self.assertEqual(str(self.user_profile1), 'John Doe (johndoe)')

    def test_user_profile_get_absolute_url(self):
        expected_url = f'/profile/{self.user_profile1.slug}/'
        self.assertEquals(self.user_profile1.get_absolute_url(), expected_url)


class TestPostModel(UserProfileCase, TagCase):

    def setUp(self):
        self.user1, self.user_profile1 = self.create_user_profile(
            'John',
            'Doe',
            'johndoe',
            'johndoe@example.com',
            'password123',
            'https://example.com/api/image',
            'Some description'
        )

        self.tags1 = self.create_tags((
            'MyTag1',
            'MyTag2',
            'MyTag3'
        ))

        self.post1 = Post.objects.create(
            user_profile=self.user_profile1,
            title='My Post Title',
            featured_image='https://example.com/image',
            content='Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            excerpt='My Post Excerpt',
        )

        self.post1.tags.set(self.tags1)

    def test_post_creation(self):
        self.assertEqual(self.post1.user_profile, self.user_profile1)
        self.assertEqual(self.post1.title, 'My Post Title')
        self.assertEqual(self.post1.featured_image,
                         'https://example.com/image')
        self.assertEqual(
            self.post1.content, 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.')
        self.assertEqual(self.post1.excerpt, 'My Post Excerpt')
        self.assertListEqual(list(self.post1.tags.all()), self.tags1)

    def test_post_get_absolute_url(self):
        expected_url = f'/post/{self.post1.slug}/'
        self.assertEquals(self.post1.get_absolute_url(), expected_url)


class TestTagModel(TagCase):

    def setUp(self):
        self.tag1 = self.create_tag(name='MyTag')

    def test_tag_creation(self):
        self.assertEqual(self.tag1.name, 'MyTag')
        self.assertEqual(self.tag1.slug, 'mytag')

    def test_post_get_absolute_url(self):
        expected_url = f'/tag/{self.tag1.slug}/'
        self.assertEquals(self.tag1.get_absolute_url(), expected_url)
