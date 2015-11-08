from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, UpdateView
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

from .models import User
from .models import StProfile
#from ..util import paginate


class UserView(ListView):
    model = User
    template_name = 'registration/users_list.html'
    context_object_name = 'users'


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = {'username', 'last_name', 'first_name', 'email', 'date_joined'}

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_action = reverse('users_edit',
            kwargs={'pk': kwargs['instance'].id})

        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        submit = Submit('save_button', _(u'Save'),
                            css_class="btn btn-primary")
        self.helper.layout = Layout(
            Fieldset(
                '',
                'username',
                'last_name',
                'first_name',
                'email',
                'date_joined',
                'user.stprofile.mobile_phone',
            ),
            ButtonHolder(
                submit
            )
        )

        self.helper.layout[-1] = ButtonHolder(
            submit,
            Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link"),
        )


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'registration/users_form.html'

    def get_success_url(self):
        return _(u'%s?status_message=Saved!' % reverse('home'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                _(u'%s?status_message=Canceled!' % reverse('home')))
        else:
            return super(UserUpdateView,
                         self).post(request, *args, **kwargs)

