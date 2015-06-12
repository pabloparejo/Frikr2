from models import Photo, PhotoComment
from django.forms import ModelForm


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        exclude = ("owner", "popularity")


class PhotoCommentForm(ModelForm):
    class Meta():
        model = PhotoComment
        fields = ("text",)
