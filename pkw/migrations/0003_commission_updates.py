# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pkw', '0002_auto_20150418_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='updates',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
