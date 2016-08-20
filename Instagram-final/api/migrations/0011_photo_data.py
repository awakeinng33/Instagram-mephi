# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20150419_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 20, 19, 31, 45, 514573, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
