# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('name', models.CharField(max_length=100, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('district_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pkw.District')),
            ],
            options={
            },
            bases=('pkw.district',),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('district_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pkw.District')),
            ],
            options={
            },
            bases=('pkw.district',),
        ),
        migrations.CreateModel(
            name='Voivodeship',
            fields=[
                ('name', models.CharField(max_length=25, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='county',
            name='city',
            field=models.ForeignKey(to='pkw.City'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commission',
            name='dist',
            field=models.ForeignKey(to='pkw.District'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='voiv',
            field=models.ForeignKey(to='pkw.Voivodeship'),
            preserve_default=True,
        ),
    ]
