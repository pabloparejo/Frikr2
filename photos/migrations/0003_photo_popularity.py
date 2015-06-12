# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0002_auto_20150603_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='popularity',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
