# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20150413_2141'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
    ]
