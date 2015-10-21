__author__ = 'travelist'
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import CreateView, UpdateView, DeleteView
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions


from ..models import Exam


# Views for Exams
def exams_list(request):
    exams = Exam.objects.all()

    # try to order exam list
    reverse_begin = False
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'title', 'teacher', 'exam_group'):
        exams = exams.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()
    else:
        exams = exams.order_by('title')
        reverse_begin = True

    # paginate students
    paginator = Paginator(exams, 4)
    page = request.GET.get('page', '1')
    number_on_page = (int(page) - 1) * 4

    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        exams = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        exams = paginator.page(paginator.num_pages)

    return render(request, 'students/exams_list.html', {'exams': exams,
                                                         'reverse_begin': reverse_begin,
                                                         'number_on_page': number_on_page})


class ExamForm(ModelForm):
    class Meta:
        model = Exam
        fields = {'title', 'date_exam', 'teacher', 'exam_group', 'notes'}

    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # add form or edit form
        if kwargs['instance'] is None:
            add_form = True
        else:
            add_form = False
        # set form tag attributes
        if add_form:
            self.helper.form_action = reverse('exams_add')
        else:
            self.helper.form_action = reverse('exams_edit', kwargs={'pk': kwargs['instance'].id})

        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        # add buttons
        if add_form:
            submit = Submit('add_button', u'Додати', css_class="btn btn-primary")
        else:
            submit = Submit('save_button', u'Зберегти', css_class="btn btn-primary")
        self.helper.layout[-1] = FormActions(
            submit,
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
        )

class BaseExamFormView(object):
    def get_success_url(self):
        return u'%s?status_message=Зміни успішно збережено!' % reverse('exams')
    def post(self, request, *args, **kwargs):
        # handle cancel button
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('exams') + u'?status_message=Зміни скасовано.')
        else:
            return super(BaseExamFormView, self).post(request, *args, **kwargs)


class ExamAddView(BaseExamFormView, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'students/exams_form.html'

class ExamUpdateView(BaseExamFormView, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'students/exams_form.html'

class ExamDeleteView(BaseExamFormView, DeleteView):
    model = Exam
    template_name = 'students/exams_confirm_delete.html'

