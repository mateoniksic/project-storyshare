from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from django.contrib.auth.models import User

from .forms import *
from django.contrib import messages

from .utils.functions import *
from urllib.parse import urlencode
from django.core.paginator import Paginator


class IndexTemplateView(generic.TemplateView):
    template_name = 'app/pages/public/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = Post.objects.all().order_by('-date_created')[:18]
        page: int = self.request.GET.get('page', 1)
        p = Paginator(posts, 6)
        posts = p.get_page(page)

        context = {
            'posts': posts,
            'posts_count': Post.objects.all().count(),
            'members_count': User.objects.all().count(),
            'tags_count': Tag.objects.all().count(),
        }

        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('app:for-you-post-list-view'))
        return super().get(request, *args, **kwargs)


class UserSignUpView(generic.CreateView):
    model = User
    form_class = CustomUserCreationForm

    template_name = 'app/pages/public/user_auth/sign_up.html'

    success_url = reverse_lazy('app:sign-in')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('app:for-you-post-list-view'))
        return super().get(request, *args, **kwargs)


class UserSignInView(LoginView):
    form_class = CustomAuthenticationForm

    template_name = 'app/pages/public/user_auth/sign_in.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(
            self.request, 'Your username or password was incorrect. Please, try again.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('app:for-you-post-list-view')


class UserSignOutView(LogoutView):
    next_page = reverse_lazy('app:sign-in')


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'app/pages/private/user/user_form/user_update_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your user settings have been updated.')
        return response

    def get_success_url(self):
        return reverse_lazy('app:user-update-view', kwargs={'pk': self.object.pk})


class SearchResultsUserListView(LoginRequiredMixin, generic.ListView):
    model = User
    context_object_name = 'users'

    template_name = 'app/pages/private/user/user_list/user_search_results.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            queryset = User.objects.filter(username__icontains=query).order_by('-username').all()
        else:
            queryset = User.objects.none()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        params_get = self.request.GET.dict()
        filtered_params = {key: value for key,
                           value in params_get.items() if key != 'page'}
        encoded_params = urlencode(filtered_params, safe='&')
        context['params'] = encoded_params + '&'

        return context


class UserProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserProfile
    context_object_name = 'user_profile'

    template_name = 'app/pages/private/user_profile/user_profile_detail/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        member = self.object.user

        posts = member.profile.posts.order_by(
            '-date_created').all()
        page: int = self.request.GET.get('page', 1)
        p = Paginator(posts, 6)
        posts = p.get_page(page)

        context.update({
            'member': member,
            'posts': posts,
        })

        user = self.request.user
        if (member == user):
            context.update({
                'member': user,
                'is_user': True,
                'user_profile_form': UserProfileForm(instance=self.object),
            })

        return context

    def post(self, request, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        request_data = self.request.POST
        form_id = request_data['form_id']

        member_follow_form_id = 'user_follow_or_unfollow_form'
        if form_id == member_follow_form_id:
            handle_user_follow_or_unfollow_form(
                request_data[f'{member_follow_form_id}-submit'],
                self.request.user.id,
                request_data[f'{member_follow_form_id}-member_id']
            )

        elif form_id == UserProfileForm().prefix:
            handle_user_profile_form(request_data, self.request.user, context)

        return render(request, self.template_name, context=context)


class FollowingPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'

    template_name = 'app/pages/private/post/post_list/following.html'
    paginate_by = 6

    def get_queryset(self):
        following = UserProfile.objects.filter(
            user=self.request.user.id).values_list('following', flat=True).all()

        queryset = Post.objects.filter(user_profile__in=following).order_by(
            '-date_created').all()

        return queryset


class ForYouPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'

    template_name = 'app/pages/private/post/post_list/for_you.html'
    paginate_by = 6

    def get_queryset(self):
        following = UserProfile.objects.filter(
            user=self.request.user.id).values_list('following', flat=True).all()

        queryset = Post.objects.exclude(user_profile__in=following).order_by(
            '-date_created').all()

        return queryset


class PostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    context_object_name = 'post'

    template_name = 'app/pages/private/post/post_detail/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        member = self.object.user_profile.user
        context['member'] = member

        user = self.request.user
        if (member == user):
            context.update({
                'member': user,
                'is_user': True,
                'user_profile_form': UserProfileForm(instance=user.profile),
            })

        return context

    def post(self, request, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        request_data = self.request.POST
        form_id = request_data['form_id']

        member_follow_form_id = 'user_follow_or_unfollow_form'
        if form_id == member_follow_form_id:
            handle_user_follow_or_unfollow_form(
                request_data[f'{member_follow_form_id}-submit'],
                self.request.user.id,
                request_data[f'{member_follow_form_id}-member_id']
            )

        elif form_id == UserProfileForm().prefix:
            handle_user_profile_form(request_data, self.request.user, context)

        return render(request, self.template_name, context=context)


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm

    template_name = 'app/pages/private/post/post_form/post_create_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm

    template_name = 'app/pages/private/post/post_form/post_update_form.html'

    def get_initial(self):
        tags = self.object.tags.all().values_list('name', flat=True)
        tag_list = ' '.join(tags)
        initial = {'tag_list': tag_list}
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse_lazy('app:post-detail-view', kwargs={'slug': self.object.slug})


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post

    def get_success_url(self):
        return reverse_lazy('app:profile-detail-view', kwargs={'slug': self.request.user.profile.slug})


class TagDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tag
    context_object_name = 'tag'

    template_name = 'app/pages/private/tag/tag_detail/tag_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = self.object.posts.order_by(
            '-date_created').all()

        page: int = self.request.GET.get('page', 1)
        p = Paginator(posts, 6)

        context['posts'] = p.get_page(page)

        return context
