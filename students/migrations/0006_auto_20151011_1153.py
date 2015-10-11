# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20151010_1142'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ball', models.IntegerField(verbose_name='\u0411\u0430\u043b')),
                ('date_exam', models.DateField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0456\u0441\u043f\u0438\u0442\u0443', blank=True)),
                ('notes', models.TextField(verbose_name='\u0414\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u0456 \u043d\u043e\u0442\u0430\u0442\u043a\u0438', blank=True)),
                ('exam_title', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='\u041f\u0440\u0435\u0434\u043c\u0435\u0442', to='students.Exam', null=True)),
            ],
            options={
                'verbose_name': '\u041e\u0446\u0456\u043d\u043a\u0430',
                'verbose_name_plural': '\u041e\u0446\u0456\u043d\u043a\u0438',
            },
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': '\u0421\u0442\u0443\u0434\u0435\u043d\u0442', 'verbose_name_plural': '\u0421\u0442\u0443\u0434\u0435\u043d\u0442\u0438'},
        ),
        migrations.AddField(
            model_name='rating',
            name='student_ball',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442', to='students.Student', null=True),
        ),
    ]
