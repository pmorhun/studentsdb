# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.views.generic import UpdateView
from django.forms import ModelForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions


from ..models import Student, Group


# Views for Students

def students_list(request):
    students = Student.objects.all()

    # try to order students list
    reverse_begin = False
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'last_name', 'first_name', 'student_group', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    else:
        students = students.order_by('last_name')
        reverse_begin = True

    # paginate students

    paginator = Paginator(students, 7)
    page = request.GET.get('page', '1')
    number_on_page = (int(page) - 1) * 7

    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html', {'students': students,
                                                           'reverse_begin': reverse_begin,
                                                           'number_on_page': number_on_page})



def students_add(request):

    # was form posted?
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get('add_button') is not None:
            # errors collection
            errors = {}
            # data for student object
            data = {'middle_name': request.POST.get('middle_name'), 'notes': request.POST.get('notes')}
            # validate user input

            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть коректну групу"
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                if photo.content_type.split('/')[0] != 'image' or photo.size > 2621440:
                    errors['photo'] = u"Оберіть правильне зображення для фото (не більше 2.5Мб)"
                else:
                    data['photo'] = photo

            # save student
            if not errors:
                student = Student(**data)
                student.save()
                # redirect to students list
                messages.info(request, u'Студента '+student.last_name+' '+student.first_name+' '+student.middle_name+u' додано!')
                return HttpResponseRedirect(reverse('home'))
            else:
                # render form with errors and previous user input
                messages.info(request, u'Будь-ласка, виправте наступні помилки')
                return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title'),
                                                                      'errors': errors})

        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            messages.info(request, u'Додавання студента скасовано!')
            return HttpResponseRedirect(reverse('home'))

    else:
        # initial form render
        return render(request, 'students/students_add.html',{'groups': Group.objects.all().order_by('title')})

class StudentUpdateForm(forms.Form):

    """
    def __init__(self, *args, **kwargs):

        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # set form tag attributes
        self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        # add buttons
        self.helper.layout[-1] = FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),      )
    """
    first_name = forms.CharField(
        max_length=128,
        label=u"Ім'я")
    #last_name = forms.CharField(
    #    max_length=256,
    #    label=u"Прізвище")
    middle_name = forms.CharField(
        max_length=256,
        label=u"По-батькові")
    birthday = forms.DateField(
        label=u"Дата народження")
    #photo = forms.ImageField(
    #    label=u"Фото")
    ticket = forms.CharField(
        max_length=25,
        label=u"Білет")
    #notes = forms.CharField(
    #    label=u"Додаткові нотатки")
    #student_group = forms.ForeignKey('Group', label=u"Група")

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        #import pdb; pdb.set_trace()
        #pdb
        self.fields['last_name'] = forms.CharField(initial=Student.objects.get(pk=request.POST['last_name']), label=u"Прізвище")


def students_edit(request, pk):
    # check if form was posted

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentUpdateForm(request.POST)
        # check whether user data is valid:
        if form.is_valid():
            # save data
            id = pk
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            middle_name = form.cleaned_data['meddle_name']
            birthday = form.cleaned_data['birthday']
            ticket = form.cleaned_data['ticket']
            Student(id, first_name, last_name, middle_name, birthday, ticket).save()
            messages.info(request, u'Success')
            return redirect('/success/')

        #if not valid
        messages.info(request, u'Виправте наступні помилки')
        return render(request, 'students/students_edit.html', {'form': form})
    # if there was not POST render blank form
    else:
        form = StudentUpdateForm()
    return render(request, 'students/students_edit.html', {'form': form})


"""
class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = {'first_name', 'last_name', 'middle_name', 'student_group', 'birthday', 'photo', 'ticket', 'notes'}

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # set form tag attributes
        self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        # add buttons
        self.helper.layout[-1] = FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),      )

class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm
    def get_success_url(self):
        return u'%s?status_message=Студента успішно збережено!' % reverse('home')
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Редагування студента відмінено!'% reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)
"""




def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
