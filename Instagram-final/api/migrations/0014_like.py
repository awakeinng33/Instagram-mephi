# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_photo_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('image', models.IntegerField(null=True, blank=True)),
                ('username', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'like',
            },
            bases=(models.Model,),
        ),
    ]
