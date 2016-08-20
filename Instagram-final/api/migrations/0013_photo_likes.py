# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_photo_comment_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
