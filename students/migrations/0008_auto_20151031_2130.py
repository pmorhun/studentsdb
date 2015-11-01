# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_monthjournal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='exam_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0413\u0440\u0443\u043f\u0430', to='students.Group', null=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='exam_title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u041f\u0440\u0435\u0434\u043c\u0435\u0442', to='students.Exam', null=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='student_ball',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442', to='students.Student', null=True),
        ),
    ]
