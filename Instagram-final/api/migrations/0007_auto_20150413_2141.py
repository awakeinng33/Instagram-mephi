# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_image'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='image',
            table='images',
        ),
    ]
