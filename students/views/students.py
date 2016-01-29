
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models import Student
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
            students = Student.objects.all()

        search = self.request.GET.get('search_quwery', '').strip()
        if search:
            students = Student.objects.filter(last_name__icontains=search)

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


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['last_name', 'first_name', 'middle_name', 'student_group',
                  'ticket', 'birthday', 'photo', 'notes', ]

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
        self.helper.label_class = 'col-sm-4 control-label'
        self.helper.field_class = 'col-sm-8'
        # add buttons
        if add_form:
            submit = Submit('add_button', _(u'Add'),
                            css_class="btn btn-primary")
        else:
            submit = Submit('add_button', _(u'Save'),
                            css_class="btn btn-primary")
        self.helper.add_input(submit)
        self.helper.add_input(Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link"))


class BaseStudentFormView(object):

    def get_success_url(self):
        return _(u'%s?status_message=Saved!' % reverse('home'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                _(u'%s?status_message=Canceled!' % reverse('home')))
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
        return _(u'%s?status_message=Delete successfully!' % reverse('home'))

