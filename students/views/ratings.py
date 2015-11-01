__author__ = 'travelist'
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import FormActions

from ..models import Rating
from ..util import paginate

class RatingView(ListView):
    model = Rating
    template_name = 'students/ratings_list.html'
    context_object_name = 'ratings'

    def get_context_data(self, **kwargs):

        # get context data from TemplateView class
        context = super(RatingView, self).get_context_data(**kwargs)

        # try to order rating list
        reverse_begin = False
        ratings = Rating.objects.all()
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('student_ball', 'exam_title', 'date_exam', 'ball'):
            ratings = ratings.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                ratings = ratings.reverse()
        else:
            ratings =ratings.order_by('student_ball')
            reverse_begin = True

        context['ratings'] = ratings
        context['reverse_begin'] = reverse_begin
        # apply pagination, 10 students per page
        context = paginate(ratings, 4, self.request, context, var_name='ratings')
        # finally return updated context
        # with paginated students
        return context


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = {'ball', 'date_exam', 'student_ball', 'exam_title', 'notes'}

    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # add form or edit form
        if kwargs['instance'] is None:
            add_form = True
        else:
            add_form = False
        # set form tag attributes
        if add_form:
            self.helper.form_action = reverse('ratings_add')
        else:
            self.helper.form_action = reverse('ratings_edit',
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
            submit = Submit('save_button', u'Зберегти',
                            css_class="btn btn-primary")

        self.helper.layout = Layout(
            Fieldset(
                'Rating students',
                'ball',
                'date_exam',
                'student_ball',
                'exam_title',
                'notes'
            ),
            ButtonHolder(
                submit
            )
        )



        self.helper.layout[-1] = ButtonHolder(
            submit,
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
        )

class BaseRatingFormView(object):

    def get_success_url(self):
        return u'%s?status_message=Зміни збережено!' % reverse('ratings')


    def post(self, request, *args, **kwargs):
        # handle cancel button
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('ratings') + u'?status_message=Зміни скасовано.')
        else:
            return super(BaseRatingFormView, self).post(request, *args, **kwargs)


class RatingAddView(BaseRatingFormView, CreateView):
    model = Rating
    form_class = RatingForm
    template_name = 'students/ratings_form.html'

class RatingUpdateView(BaseRatingFormView, UpdateView):
    model = Rating
    form_class = RatingForm
    template_name = 'students/ratings_form.html'

class RatingDeleteView(DeleteView):
    model = Rating
    template_name = 'students/ratings_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message=Оцінку видалено!' % reverse('ratings')