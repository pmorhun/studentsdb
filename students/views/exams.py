__author__ = 'travelist'
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions


from ..models import Exam
from ..util import paginate

# Views for Exams
class ExamView(ListView):
    model = Exam
    template_name = 'students/exams_list.html'
    context_object_name = 'exams'

    def get_context_data(self, **kwargs):

        # get context data from TemplateView class
        context = super(ExamView, self).get_context_data(**kwargs)

        # try to order rating list
        reverse_begin = False
        exams = Exam.objects.all()
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('title', 'date_exam', 'teacher', 'exam_group'):
            exams = exams.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                exams = exams.reverse()
        else:
            exams = exams.order_by('title')
            reverse_begin = True

        context['exams'] = exams
        context['reverse_begin'] = reverse_begin
        # apply pagination, 10 students per page
        context = paginate(exams, 4, self.request, context, var_name='exams')
        # finally return updated context
        # with paginated students
        return context


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

