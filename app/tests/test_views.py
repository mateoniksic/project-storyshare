from django.test import TestCase, Client
from django.urls import reverse

from app.views import *

from app.models import *
from django.contrib.auth.models import User


class TestIndexTemplateViewCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser', password=self.user_password)

        self.url = reverse('app:index-template-view')
        self.redirect_authenticated_user_url = reverse(
            'app:for-you-post-list-view')

        self.template = 'app/pages/public/index.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_authenticated_user_is_redirected(self):
        self.client.login(username=self.user.username,
                          password=self.user_password)
        response = self.client.get(self.url)
        self.assertRedirects(response, self.redirect_authenticated_user_url)


class TestUserSignUpViewCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser', password=self.user_password)

        self.url = reverse('app:sign-up')
        self.success_url = reverse('app:sign-in')
        self.redirect_authenticated_user_url = reverse(
            'app:for-you-post-list-view')

        self.template = 'app/pages/public/user_auth/sign_up.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_custom_user_creation_form_valid(self):
        data = {
            'custom_user_creation_form-username': 'testuser1',
            'custom_user_creation_form-first_name': 'testfirstname',
            'custom_user_creation_form-last_name': 'testlastname',
            'custom_user_creation_form-email': 'testuser@testdomain.com',
            'custom_user_creation_form-password1': 'testpassword',
            'custom_user_creation_form-password2': 'testpassword',
        }
        response = self.client.post(self.url, data=data)
        self.assertTrue(User.objects.filter(username='testuser1').exists())
        self.assertRedirects(response, self.success_url)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_is_redirected(self):
        self.client.login(username=self.user.username,
                          password=self.user_password)
        response = self.client.get(self.url)
        self.assertRedirects(response, self.redirect_authenticated_user_url)


class TestUserSignInViewCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser', password=self.user_password)

        self.url = reverse('app:sign-in')
        self.success_url = reverse('app:for-you-post-list-view')
        self.redirect_authenticated_user_url = reverse(
            'app:for-you-post-list-view')

        self.template = 'app/pages/public/user_auth/sign_in.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_custom_authentication_form_valid(self):
        data = {
            'custom_authentication_form-username': self.user.username,
            'custom_authentication_form-password': 'testpassword',
        }
        response = self.client.post(self.url, data=data)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertRedirects(response, self.success_url)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_is_redirected(self):
        self.client.login(username=self.user.username,
                          password=self.user_password)
        response = self.client.get(self.url)
        self.assertRedirects(response, self.redirect_authenticated_user_url)


class TestUserSignOutViewCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser', password=self.user_password)

        self.url = reverse('app:sign-out')
        self.next_page = reverse('app:sign-in')
        self.redirect_authenticated_user_url = reverse(
            'app:for-you-post-list-view')

    def test_get(self):
        self.client.login(username=self.user.username,
                          password=self.user_password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.next_page)
        self.assertFalse('_auth_user_id' in self.client.session)


class TestUserUpdateViewCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser', password=self.user_password)

        self.url = reverse('app:user-update-view', kwargs={'pk': self.user.id})
        self.success_url = reverse(
            'app:user-update-view', kwargs={'pk': self.user.id})

        self.template = 'app/pages/private/user/user_form/user_update_form.html'

    def test_get(self):
        self.client.login(username=self.user.username,
                          password=self.user_password)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

    def test_user_update_form_valid(self):
        self.client.login(username=self.user.username,
                          password=self.user_password)
        data = {
            'user_update_form-username': 'testusername',
            'user_update_form-first_name': 'testfirstname',
            'user_update_form-last_name': 'testlastname',
            'user_update_form-email': 'testuser@testdomain.com',
        }
        response = self.client.post(self.url, data=data)
        self.assertTrue(User.objects.filter(username='testusername').exists())
        self.assertRedirects(response, self.success_url)
        self.assertEqual(response.status_code, 302)

    def test_user_update_form_invalid(self):
        self.client.login(username=self.user.username,
                          password=self.user_password)
        data = {
            'user_update_form-username': 'testusername',
            'user_update_form-first_name': 'testfirstname',
            'user_update_form-last_name': 'testlastname',
            'user_update_form-email': 'notemail',
        }
        response = self.client.post(self.url, data=data)
        self.assertFalse(User.objects.filter(username='testusername').exists())
        self.assertEqual(response.status_code, 200)


class TestUserSearchResultsUserListViewCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser', password=self.user_password)
        self.client.login(username=self.user.username,
                          password=self.user_password)

        self.url = reverse('app:search-results-user-list-view')

        self.template = 'app/pages/private/user/user_list/user_search_results.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_search_form_valid(self):
        User.objects.create_user(
            username='testmember', password=self.user_password)
        response = self.client.get(self.url, data={'q': 'testmember'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testmember')

    def test_search_form_invalid(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'testmember')


class TestUserProfileDetailViewCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser', password=self.user_password)
        self.client.login(username=self.user.username,
                          password=self.user_password)

        self.url = reverse('app:profile-detail-view',
                           kwargs={'slug': self.user.profile.slug})

        self.template = 'app/pages/private/user_profile/user_profile_detail/profile_detail.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_user_follow_or_unfollow_form_valid_follow(self):
        member = User.objects.create_user(
            username='testmember', password=self.user_password)
        data = {
            'form_id': 'user_follow_or_unfollow_form',
            'user_follow_or_unfollow_form-member_id': member.id,
            'user_follow_or_unfollow_form-submit': 'follow',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(member.profile, self.user.profile.following.all())

    def test_user_follow_or_unfollow_form_valid_unfollow(self):
        member = User.objects.create_user(
            username='testmember', password=self.user_password)
        self.user.profile.following.add(member.profile)
        data = {
            'form_id': 'user_follow_or_unfollow_form',
            'user_follow_or_unfollow_form-member_id': member.id,
            'user_follow_or_unfollow_form-submit': 'unfollow',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(member.profile, self.user.profile.following.all())

    def test_user_profile_form_valid(self):
        data = {
            'form_id': 'user_profile_form',
            'user_profile_form-profile_image': 'https://www.example.com/api/profile-image',
            'user_profile_form-description': 'Test description'
        }
        response = self.client.post(self.url, data=data)
        self.user.profile.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEquals(self.user.profile.profile_image,
                          'https://www.example.com/api/profile-image')
        self.assertEquals(self.user.profile.description,
                          'Test description')


class TestFollowingPostListViewCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser', password=self.user_password)
        self.client.login(username=self.user.username,
                          password=self.user_password)

        self.url = reverse('app:following-post-list-view')

        self.template = 'app/pages/private/post/post_list/following.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)


class TestForYouPostListViewCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser', password=self.user_password)
        self.client.login(username=self.user.username,
                          password=self.user_password)

        self.url = reverse('app:for-you-post-list-view')

        self.template = 'app/pages/private/post/post_list/for_you.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)


class TestForYouPostListViewCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser', password=self.user_password)
        self.client.login(username=self.user.username,
                          password=self.user_password)

        self.post = Post.objects.create(
            user_profile=self.user.profile,
            title='Post Title',
            featured_image='https://wwww.example.com/api/image',
            content='Post content. ' * 100,
            excerpt='Post excerpt. ' * 20,
        )

        self.post.tags.add(Tag.objects.create(name='test'))

        self.url = reverse('app:post-detail-view',
                           kwargs={'slug': self.post.slug})

        self.template = 'app/pages/private/post/post_detail/post_detail.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_user_follow_or_unfollow_form_valid_follow(self):
        member = User.objects.create_user(
            username='testmember', password=self.user_password)
        data = {
            'form_id': 'user_follow_or_unfollow_form',
            'user_follow_or_unfollow_form-member_id': member.id,
            'user_follow_or_unfollow_form-submit': 'follow',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(member.profile, self.user.profile.following.all())

    def test_user_follow_or_unfollow_form_valid_unfollow(self):
        member = User.objects.create_user(
            username='testmember', password=self.user_password)
        self.user.profile.following.add(member.profile)
        data = {
            'form_id': 'user_follow_or_unfollow_form',
            'user_follow_or_unfollow_form-member_id': member.id,
            'user_follow_or_unfollow_form-submit': 'unfollow',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(member.profile, self.user.profile.following.all())

    def test_user_profile_form_valid(self):
        data = {
            'form_id': 'user_profile_form',
            'user_profile_form-profile_image': 'https://www.example.com/api/profile-image',
            'user_profile_form-description': 'Test description'
        }
        response = self.client.post(self.url, data=data)
        self.user.profile.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEquals(self.user.profile.profile_image,
                          'https://www.example.com/api/profile-image')
        self.assertEquals(self.user.profile.description,
                          'Test description')


class TestPostCreateViewCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser', password=self.user_password)
        self.client.login(username=self.user.username,
                          password=self.user_password)

        self.url = reverse('app:post-create-view')

        self.template = 'app/pages/private/post/post_form/post_create_form.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_post_form_valid(self):
        data = {
            'form_id': 'post_form',
            'post_form-title': 'Post Title',
            'post_form-featured_image': 'https://wwww.example.com/api/image',
            'post_form-content': 'Post content. ' * 100,
            'post_form-excerpt': 'Post excerpt. ' * 20,
            'post_form-tag_list': 'tag1 tag2 #/&t$a&g#3'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='Post Title').exists())


class TestPostUpdateViewCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser', password=self.user_password)
        self.client.login(username=self.user.username,
                          password=self.user_password)

        self.post = Post.objects.create(
            user_profile=self.user.profile,
            title='Post Title',
            featured_image='https://wwww.example.com/api/image',
            content='Post content. ' * 100,
            excerpt='Post excerpt. ' * 20,
        )

        self.post.tags.add(Tag.objects.create(name='test'))

        self.url = reverse('app:post-update-view',
                           kwargs={'slug': self.post.slug})

        self.template = 'app/pages/private/post/post_form/post_update_form.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_post_form_valid(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Post Title')
        self.assertContains(response, 'https://wwww.example.com/api/image')
        self.assertContains(response, 'Post content. ' * 100)
        self.assertContains(response, 'Post excerpt. ' * 20)

        data = {
            'form_id': 'post_form',
            'post_form-title': 'Post Title Updated',
            'post_form-featured_image': 'https://wwww.example.com/api/image',
            'post_form-content': 'Post content. ' * 100,
            'post_form-excerpt': 'Post excerpt. ' * 20,
            'post_form-tag_list': 'tag1 tag2 #/&t$a&g#3 newtag'
        }
        response = self.client.post(self.url, data=data)

        self.post.refresh_from_db()

        success_url = reverse('app:post-detail-view',
                              kwargs={'slug': self.post.slug})
        self.assertRedirects(response, success_url)
        self.assertEqual(self.post.title, 'Post Title Updated')
        self.assertEqual(list(self.post.tags.values_list(
            'name', flat=True)), ['tag1', 'tag2', 'tag3', 'newtag'])


class TestPostDeleteViewCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser', password=self.user_password)
        self.client.login(username=self.user.username,
                          password=self.user_password)

        self.post = Post.objects.create(
            user_profile=self.user.profile,
            title='Post Title',
            featured_image='https://wwww.example.com/api/image',
            content='Post content. ' * 100,
            excerpt='Post excerpt. ' * 20,
        )

        self.post.tags.add(Tag.objects.create(name='test'))

        self.url = reverse('app:post-delete-view',
                           kwargs={'slug': self.post.slug})
        self.success_url = reverse(
            'app:profile-detail-view', kwargs={'slug': self.user.profile.slug})
        
        self.template = None

    def test_post_delete_form_valid(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)


class TestTagDetailViewCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser', password=self.user_password)
        self.client.login(username=self.user.username,
                          password=self.user_password)
        
        self.tag = Tag.objects.create(name='tag')

        self.url = reverse('app:tag-detail-view',
                           kwargs={'slug': self.tag.slug})

        self.template = 'app/pages/private/tag/tag_detail/tag_detail.html'

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
