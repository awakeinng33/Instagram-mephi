# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.IntegerField(null=True, blank=True)),
                ('username', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'dislike',
            },
            bases=(models.Model,),
        ),
    ]
