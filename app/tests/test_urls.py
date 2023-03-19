from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app.views import *


class TestUrls(SimpleTestCase):

    def test_index_template_view_is_resolved(self):
        url = reverse('app:index-template-view')
        self.assertEquals(resolve(url).func.view_class, IndexTemplateView)


class TestUserUrls(SimpleTestCase):

    def test_sign_up_is_resolved(self):
        url = reverse('app:sign-up')
        self.assertEquals(resolve(url).func.view_class, UserSignUpView)

    def test_sign_in_is_resolved(self):
        url = reverse('app:sign-in')
        self.assertEquals(resolve(url).func.view_class, UserSignInView)

    def test_sign_out_is_resolved(self):
        url = reverse('app:sign-out')
        self.assertEquals(resolve(url).func.view_class, UserSignOutView)

    def test_user_update_view_is_resolved(self):
        url = reverse('app:user-update-view', args=['0'])
        self.assertEquals(resolve(url).func.view_class, UserUpdateView)

    def test_search_results_user_list_view_is_resolved(self):
        url = reverse('app:search-results-user-list-view')
        self.assertEquals(resolve(url).func.view_class,
                          SearchResultsUserListView)


class TestUserProfileUrls(SimpleTestCase):

    def test_profile_detail_view_is_resolved(self):
        url = reverse('app:profile-detail-view', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, UserProfileDetailView)


class TestPostUrls(SimpleTestCase):

    def test_for_you_post_list_view_is_resolved(self):
        url = reverse('app:for-you-post-list-view')
        self.assertEquals(resolve(url).func.view_class, ForYouPostListView)

    def test_following_post_list_view_is_resolved(self):
        url = reverse('app:following-post-list-view')
        self.assertEquals(resolve(url).func.view_class, FollowingPostListView)

    def test_post_detail_view_is_resolved(self):
        url = reverse('app:post-detail-view', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, PostDetailView)

    def test_post_create_view_is_resolved(self):
        url = reverse('app:post-create-view')
        self.assertEquals(resolve(url).func.view_class, PostCreateView)

    def test_post_update_view_is_resolved(self):
        url = reverse('app:post-update-view', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, PostUpdateView)

    def test_post_delete_view_is_resolved(self):
        url = reverse('app:post-delete-view', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, PostDeleteView)


class TestTagUrls(SimpleTestCase):

    def test_tag_detail_view_is_resolved(self):
        url = reverse('app:tag-detail-view', args=['slug'])
        self.assertEquals(resolve(url).func.view_class, TagDetailView)
