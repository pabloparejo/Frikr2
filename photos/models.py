from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Photo(models.Model):

    # Visibility Consts
    PUBLICA = "PUB"
    PRIVADA = "PRI"

    VISIBILITY = ((PUBLICA, "Publica"),
                  (PRIVADA, "Privada"),
                  )

    owner = models.ForeignKey(User)

    name = models.CharField(max_length=250)
    pub_date = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    url = models.URLField()
    popularity = models.IntegerField(default=0)
    visibility = models.CharField(max_length=3, choices=VISIBILITY, default=PUBLICA)

    def __unicode__(self):
        return self.name


class PhotoComment(models.Model):

    user = models.ForeignKey(User, related_name='comments')
    photo = models.ForeignKey(Photo, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)

    text = models.TextField(verbose_name='')
