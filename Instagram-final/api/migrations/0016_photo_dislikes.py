# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_dislike'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='dislikes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
