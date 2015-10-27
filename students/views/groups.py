# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions


from ..models import Group, Student
from ..util import paginate, get_current_group

# Views for Groups
class GroupView(ListView):
    model = Group
    template_name = 'students/groups_list.html'
    context_object_name = 'groups'


    def get_queryset(self):
        # check if we need to show only one group of students
        current_group = get_current_group(self.request)
        if current_group:
            groups = [current_group]
        else:
            # otherwise show all students
            groups = Group.objects.all()
            # try to order rating list
            #reverse_begin = False
            order_by = self.request.GET.get('order_by', '')
            if order_by in ('title', 'leader'):
                groups = groups.order_by(order_by)
                if self.request.GET.get('reverse', '') == '1':
                    groups = groups.reverse()
            else:
                groups = groups.order_by('title')
                #reverse_begin = True
        return groups


    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(GroupView, self).get_context_data(**kwargs)
        reverse_begin = True
        context['reverse_begin'] = reverse_begin
        # apply pagination, 10 students per page
        context = paginate(context['groups'], 4, self.request, context, var_name='groups')
        # finally return updated context
        # with paginated students
        return context



class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = {'title', 'leader', 'notes'}

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # add form or edit form
        if kwargs['instance'] is None:
            add_form = True
        else:
            add_form = False
        # set form tag attributes
        if add_form:
            self.helper.form_action = reverse('groups_add')
        else:
            self.helper.form_action = reverse('groups_edit', kwargs={'pk': kwargs['instance'].id})

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

class BaseGroupFormView(object):
    def get_success_url(self):
        return u'%s?status_message=Зміни успішно збережено!' % reverse('groups')
    def post(self, request, *args, **kwargs):
        # handle cancel button
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('groups') + u'?status_message=Зміни скасовано.')
        else:
            return super(BaseGroupFormView, self).post(request, *args, **kwargs)


class GroupAddView(BaseGroupFormView, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'students/groups_form.html'

class GroupUpdateView(BaseGroupFormView, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'students/groups_form.html'

class GroupDeleteView(BaseGroupFormView, DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'



