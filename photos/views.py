from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from models import Photo, PhotoComment
from forms import PhotoForm, PhotoCommentForm
from django.views.generic import View, ListView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.db.models import Q


class PhotoListView(ListView):
    model = Photo
    template_name = "photos/home.html"

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous():
            return Photo.objects.filter(visibility=Photo.PUBLICA)
        elif user.is_staff:
            return Photo.objects.all()
        else:
            #usuario registrado
            return Photo.objects.filter(Q(owner=user) | Q(visibility=Photo.PUBLICA))


class PhotoDetailView(View):

    def get(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        form = PhotoCommentForm()
        detail = True
        return render(request, 'photos/detail.html', locals())

    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        instance = PhotoComment(user=request.user, photo=photo)
        form = PhotoCommentForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("photo_detail", pk)

        return render(request, 'photos/detail.html', locals())


class NewPhotoView(View):
    @method_decorator(login_required(login_url="login"))
    def get(self, request):
        form = PhotoForm()
        context = {"form": form}
        return render(request, 'photos/new_photo.html', context)

    @method_decorator(login_required(login_url="login"))
    def post(self, request):
        photo = Photo(owner=request.user)
        form = PhotoForm(request.POST, instance=photo)

        if form.is_valid():
            form.save()

            return redirect("photo_detail",  photo.pk)

        context = {"form": form}
        return render(request, 'photos/new_photo.html', context)


class PhotoDeleteView(DeleteView):
    model = Photo
    success_url = reverse_lazy("photos")


class SearchView(View):

    def get(self, request):
        search = request.GET.get("search", "")

        photos = Photo.objects.filter(Q(name__icontains=search) | Q(owner__username__icontains=search))
        users = User.objects.exclude(pk=request.user.pk).filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))

        return render(request, "photos/search.html", locals())


class VoteView(View):

    def get(self, request, pk, vote):
        photo = get_object_or_404(Photo, pk=pk)
        vote = int(vote)
        photo.popularity += vote
        photo.save()
        next = request.GET.get("next", "photos")

        return redirect(next)
