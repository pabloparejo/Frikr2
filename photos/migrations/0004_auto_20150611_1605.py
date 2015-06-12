# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_photo_popularity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='popularity',
            field=models.IntegerField(default=0),
        ),
    ]
