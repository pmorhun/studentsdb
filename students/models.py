
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Student(models.Model):
    """Student Model"""

    class Meta(object):
        """ For translate model Student in admin interface"""
        verbose_name = _(u"Student")
        verbose_name_plural = _(u"Students")

    first_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"First Name"))
    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Last Name"))
    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=_(u"Middle Name"),
        default='')
    birthday = models.DateField(
        blank=True,
        verbose_name=_(u"Birthday"),
        null=True)
    photo = models.ImageField(
        blank=True,
        verbose_name=_(u"Photo"),
        null=True)
    ticket = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Ticket"))
    notes = models.TextField(
        blank=True,
        verbose_name=_(u"Note"))
    student_group = models.ForeignKey('Group',
        verbose_name=_(u"Group"),
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
        verbose_name = _(u'Journal')
        verbose_name_plural = _(u'Journals')

    student = models.ForeignKey('Student', verbose_name=_(u'Student'), blank=False, unique_for_month='date')
    # we only need year and month, so always set day to first day of the month
    date = models.DateField(verbose_name=_(u'Date'), blank=False)
    #list of days, each says whether student was present or not
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
        verbose_name = _(u"Group")
        verbose_name_plural = _(u"Groups")

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Title"))
    leader = models.OneToOneField('Student',
        verbose_name=_(u"Leader"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    notes = models.TextField(
        blank=True,
        verbose_name=_(u"Note"))

    def __unicode__(self):
        if self.leader:
            return u"%s (%s %s)" % (self.title, self.leader.first_name, self.leader.last_name)
        else:
            return u"%s" % (self.title,)

class Exam(models.Model):
    """examination Model"""
    class Meta(object):
        verbose_name = _(u"Exam")
        verbose_name_plural = _(u"Exams")

    title = models.CharField(
        max_length=256,
        verbose_name=_(u"Discipline"),
        blank=False)
    date_exam = models.DateField(
        verbose_name=_(u"Date"),
        blank=True,
        null=True)
    teacher = models.CharField(
        max_length=256,
        verbose_name=_(u"Teacher"),
        blank=True,
        null=True)
    exam_group = models.ForeignKey('Group',
        verbose_name=_(u"Group"),
        blank=False,
        null=True,
        on_delete=models.SET_NULL)
    notes = models.TextField(
        blank=True,
        verbose_name=_(u"Note"))


    def __unicode__(self):
        return u"%s" % (self.title)


class Rating(models.Model):
    """Rating examination Model"""
    class Meta(object):
        verbose_name = _(u"Rating")
        verbose_name_plural = _(u"Ratings")

    ball = models.IntegerField(
        verbose_name=_(u"Rating"),
        blank=False)
    date_exam = models.DateField(
        verbose_name=_(u"Date"),
        blank=True,
        null=True)
    student_ball = models.ForeignKey('Student',
        verbose_name=_(u"Student"),
        blank=False,
        null=True,
        on_delete=models.SET_NULL)
    exam_title = models.ForeignKey('Exam',
        verbose_name=_(u"Discipline"),
        blank=False,
        null=True,
        on_delete=models.SET_NULL)
    notes = models.TextField(
        blank=True,
        verbose_name=_(u"Note"))


    def __unicode__(self):
        return u"%s - %s" % (self.ball, self.exam_title )
