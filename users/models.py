from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(User)

    photo = models.FileField(upload_to="profile", default="img/default.jpg", verbose_name='Cargar nueva foto')
    following = models.ManyToManyField("self", symmetrical=False, related_name='followers')
