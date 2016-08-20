# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_comment_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='username',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
