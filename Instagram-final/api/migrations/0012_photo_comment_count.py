# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_photo_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='comment_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
