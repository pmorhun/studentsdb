# -*- coding: utf-8 -*-
from django.db import models


class Student(models.Model):
    """Student Model"""

    class Meta(object):
        """ For translate model Student in admin interface"""
        verbose_name = u"Студент"
        verbose_name_plural = u"Студенти"

    first_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Ім'я")
    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Прізвище")
    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"По-батькові",
        default='')
    birthday = models.DateField(
        blank=True,
        verbose_name=u"Дата народження",
        null=True)
    ticket = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Білет")
    notes = models.TextField(
        blank=True,
        verbose_name=u"Додаткові нотатки")

    def __unicode__(self):
        """
        :return: student name in django admin
        """
        return u"%s %s" % (self.first_name, self.last_name)
    