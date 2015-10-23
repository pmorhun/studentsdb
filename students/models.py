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
    photo = models.ImageField(
        blank=True,
        verbose_name=u"Фото",
        null=True)
    ticket = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Білет")
    notes = models.TextField(
        blank=True,
        verbose_name=u"Додаткові нотатки")
    student_group = models.ForeignKey('Group',
        verbose_name=u"Група",
        blank=False,
        null=True,
        on_delete=models.PROTECT)


    def __unicode__(self):
        """
        :return: student name in django admin
        """
        return u"%s %s" % (self.last_name, self.first_name)


class MonthJournal(models.Model):
    """Student Monthly Journal"""
    class Meta:
        verbose_name = u'Місячний Журнал'
        verbose_name_plural = u'Місячні Журнали'

    student = models.ForeignKey('Student', verbose_name=u'Студент', blank=False, unique_for_month='date')
    # we only need year and month, so always set day to first day of the month
    date = models.DateField(verbose_name=u'Дата', blank=False)
    # list of days, each says whether student was presenе or not
    present_day1 = models.BooleanField(default=False)
    present_day2 = models.BooleanField(default=False)
    present_day3 = models.BooleanField(default=False)
    present_day4 = models.BooleanField(default=False)
    present_day5 = models.BooleanField(default=False)
    present_day6 = models.BooleanField(default=False)
    present_day7 = models.BooleanField(default=False)
    present_day8 = models.BooleanField(default=False)
    present_day9 = models.BooleanField(default=False)
    present_day10 = models.BooleanField(default=False)
    present_day11 = models.BooleanField(default=False)
    present_day12 = models.BooleanField(default=False)
    present_day13 = models.BooleanField(default=False)
    present_day14 = models.BooleanField(default=False)
    present_day15 = models.BooleanField(default=False)
    present_day16 = models.BooleanField(default=False)
    present_day17 = models.BooleanField(default=False)
    present_day18 = models.BooleanField(default=False)
    present_day19 = models.BooleanField(default=False)
    present_day20 = models.BooleanField(default=False)
    present_day21 = models.BooleanField(default=False)
    present_day22 = models.BooleanField(default=False)
    present_day23 = models.BooleanField(default=False)
    present_day24 = models.BooleanField(default=False)
    present_day25 = models.BooleanField(default=False)
    present_day26 = models.BooleanField(default=False)
    present_day27 = models.BooleanField(default=False)
    present_day28 = models.BooleanField(default=False)
    present_day29 = models.BooleanField(default=False)
    present_day30 = models.BooleanField(default=False)
    present_day31 = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s: %d, %d' % (self.student.last_name, self.date.month, self.date.year)




class Group(models.Model):
    """Group Model"""
    class Meta(object):
        verbose_name = u"Група"
        verbose_name_plural = u"Групи"

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва")
    leader = models.OneToOneField('Student',
        verbose_name=u"Староста",
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    notes = models.TextField(
        blank=True,
        verbose_name=u"Додаткові нотатки")

    def __unicode__(self):
        if self.leader:
            return u"%s (%s %s)" % (self.title, self.leader.first_name, self.leader.last_name)
        else:
            return u"%s" % (self.title,)

class Exam(models.Model):
    """examination Model"""
    class Meta(object):
        verbose_name = u"Іспит"
        verbose_name_plural = u"Іспити"

    title = models.CharField(
        max_length=256,
        verbose_name=u"Назва предмету",
        blank=False)
    date_exam = models.DateField(
        verbose_name=u"Дата іспиту",
        blank=True,
        null=True)
    teacher = models.CharField(
        max_length=256,
        verbose_name=u"Викладач",
        blank=True,
        null=True)
    exam_group = models.ForeignKey('Group',
        verbose_name=u"Група",
        blank=False,
        null=True,
        on_delete=models.PROTECT)
    notes = models.TextField(
        blank=True,
        verbose_name=u"Додаткові нотатки")


    def __unicode__(self):
        return u"%s" % (self.title)


class Rating(models.Model):
    """Rating examination Model"""
    class Meta(object):
        verbose_name = u"Оцінка"
        verbose_name_plural = u"Оцінки"

    ball = models.IntegerField(
        verbose_name=u"Бал",
        blank=False)
    date_exam = models.DateField(
        verbose_name=u"Дата іспиту",
        blank=True,
        null=True)
    student_ball = models.ForeignKey('Student',
        verbose_name=u"Студент",
        blank=False,
        null=True,
        on_delete=models.PROTECT)
    exam_title = models.ForeignKey('Exam',
        verbose_name=u"Предмет",
        blank=False,
        null=True,
        on_delete=models.PROTECT)
    notes = models.TextField(
        blank=True,
        verbose_name=u"Додаткові нотатки")


    def __unicode__(self):
        return u"%s - %s" % (self.ball, self.exam_title )
