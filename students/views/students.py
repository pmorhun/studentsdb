# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models import Student, Group
from ..util import paginate, get_current_group


# Views for Students
class StudentView(ListView):
    model = Student
    template_name = 'students/students_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        # check if we need to show only one group of students
        current_group = get_current_group(self.request)
        if current_group:
            students = Student.objects.filter(student_group=current_group)
        else:
            # otherwise show all students
            students = Student.objects.all()

        # try to order students list
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('last_name', 'first_name', 'student_group', 'ticket'):
            students = students.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                students = students.reverse()
        else:
            students = students.order_by('last_name')

        return students


    def get_context_data(self, **kwargs):
        # context with paginated students
        context = super(StudentView, self).get_context_data(**kwargs)
        context = paginate(context['students'], 7, self.request,
                           context, var_name='students')
        return context


"""
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
"""


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = {'first_name', 'last_name', 'middle_name', 'student_group',
                  'birthday', 'photo', 'ticket', 'notes'}

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        if kwargs['instance'] is None:
            add_form = True
            self.helper.form_action = reverse('students_add')
        else:
            add_form = False
            self.helper.form_action = reverse('students_edit',
                kwargs={'pk': kwargs['instance'].id})


        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        # add buttons
        if add_form:
            submit = Submit('add_button', u'Додати',
                            css_class="btn btn-primary")
        else:
            submit = Submit('add_button', u'Зберегти',
                            css_class="btn btn-primary")

        self.helper.layout[-1] = FormActions(submit, Submit('cancel_button',
                                 u'Скасувати', css_class="btn btn-link"),)


class BaseStudentFormView(object):

    def get_success_url(self):
        return u'%s?status_message=Студента успішно збережено!' \
               % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?status_message=Редагування студента відмінено!'
                % reverse('home'))
        else:
            return super(BaseStudentFormView,
                         self).post(request, *args, **kwargs)


class StudentAddView(BaseStudentFormView, CreateView):
    model = Student
    template_name = 'students/students_form.html'
    form_class = StudentForm


class StudentUpdateView(BaseStudentFormView, UpdateView):
    model = Student
    template_name = 'students/students_form.html'
    form_class = StudentForm


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'
    def get_success_url(self):
        return u'%s?status_message=Студента успішно видалено!' % reverse('home')
