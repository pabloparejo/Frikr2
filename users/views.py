#encoding:UTF-8
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.views.generic import View, FormView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from forms import LoginForm, ProfileForm
from django.contrib.auth.forms import UserCreationForm
from models import Profile


class FollowView(View):
    @method_decorator(login_required(login_url="login"))
    def get(self, request, toggle, pk):
        user = request.user
        followed = get_object_or_404(Profile, pk=pk)

        if toggle == "follow":
            user.profile.following.add(followed)
        else:
            user.profile.following.remove(followed)

        next = request.GET.get('next', reverse_lazy('profile', args=[pk]))
        return redirect(next)


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        context = {"form": form}
        return render(request, "users/login.html", context)

    def post(self, request):
        form = LoginForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            username = form.cleaned_data.get("username", "")
            password = form.cleaned_data.get("password", "")
            user = authenticate(username=username, password=password)

            if user:
                django_login(request, user)
                url = request.GET.get("next", "photos")
                return redirect(url)

            else:
                context["error"] = "Usuario o contraseña incorrectos"

        return render(request, "users/login.html", context)


def logout(request):
    django_logout(request)
    return redirect("photos")


class ProfileView(View):
    def get(self, request, pk=None):
        form = None
        self_profile = False

        user_pk = pk or request.user.pk
        user = get_object_or_404(User, pk=user_pk)

        if not pk or int(pk) == request.user.pk:
            form = ProfileForm()
            self_profile = True

        photos = user.photo_set.all()

        context = {"photos": photos, "form": form, "user": user, "self_profile": self_profile}
        return render(request, "users/profile.html", context)

    def post(self, request, pk=None):
        if request.user.is_authenticated():
            user = Profile.objects.get_or_create(user=request.user)[0]
            form = ProfileForm(request.POST, request.FILES or None, instance=user)
            if form.is_valid():
                form.save()

        return redirect("profile")


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username", "")
        password = form.cleaned_data.get("password1", "")
        user = authenticate(username=username, password=password)

        Profile.objects.create(user=user)

        django_login(self.request, user)

        return redirect("photos")


class UsersView(ListView):
    model = User
    template_name = "users/home.html"

    def get_queryset(self):

        list_type = self.kwargs.get("list_type", None)
        profile_pk = self.kwargs.get("pk", None)
        if profile_pk and list_type:
            profile = get_object_or_404(Profile, pk=profile_pk)

        if list_type == "followers":
            return User.objects.filter(profile__in=profile.followers.all())
        elif list_type == "following":
            return User.objects.filter(profile__in=profile.following.all())
        else:
            return User.objects.exclude(pk=self.request.user.pk)
