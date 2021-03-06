# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 08:24
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tickets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='�w������')),
                ('bought_at', models.DateTimeField(auto_now_add=True, verbose_name='�w����')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='tickets.Ticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '�w������',
                'verbose_name_plural': '�w������',
                'db_table': 'purchase',
            },
        ),
    ]
