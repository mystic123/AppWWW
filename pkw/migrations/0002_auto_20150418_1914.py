# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pkw', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='allowed_vote',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commission',
            name='nr',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commission',
            name='recv_votes',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
