# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_auto_20151031_2130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exam',
            options={'verbose_name': 'Exam', 'verbose_name_plural': 'Exams'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Group', 'verbose_name_plural': 'Groups'},
        ),
        migrations.AlterModelOptions(
            name='monthjournal',
            options={'verbose_name': 'Journal', 'verbose_name_plural': 'Journals'},
        ),
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name': 'Rating', 'verbose_name_plural': 'Ratings'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
        migrations.AlterField(
            model_name='exam',
            name='date_exam',
            field=models.DateField(null=True, verbose_name='Date', blank=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Group', to='students.Group', null=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='notes',
            field=models.TextField(verbose_name='Note', blank=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='teacher',
            field=models.CharField(max_length=256, null=True, verbose_name='Teacher', blank=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Discipline'),
        ),
        migrations.AlterField(
            model_name='group',
            name='leader',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='students.Student', verbose_name='Leader'),
        ),
        migrations.AlterField(
            model_name='group',
            name='notes',
            field=models.TextField(verbose_name='Note', blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='monthjournal',
            name='date',
            field=models.DateField(verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='monthjournal',
            name='student',
            field=models.ForeignKey(unique_for_month=b'date', verbose_name='Student', to='students.Student'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='ball',
            field=models.IntegerField(verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='date_exam',
            field=models.DateField(null=True, verbose_name='Date', blank=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='exam_title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Discipline', to='students.Exam', null=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='notes',
            field=models.TextField(verbose_name='Note', blank=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='student_ball',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Student', to='students.Student', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='birthday',
            field=models.DateField(null=True, verbose_name='Birthday', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=256, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=256, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='middle_name',
            field=models.CharField(default=b'', max_length=256, verbose_name='Middle Name', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='notes',
            field=models.TextField(verbose_name='Note', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(upload_to=b'', null=True, verbose_name='Photo', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Group', to='students.Group', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='ticket',
            field=models.CharField(max_length=256, verbose_name='Ticket'),
        ),
    ]
