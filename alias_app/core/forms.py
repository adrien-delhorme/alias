from django import forms
from django.conf import settings
from django.core.mail import send_mail
from schematics.exceptions import ValidationError
from .models.alias import is_email_left_part as is_email_left_part_test


def is_email_left_part(value):
    try:
        return is_email_left_part_test(value)
    except ValidationError, e:
        raise forms.ValidationError(e.message)


class AliasForm(forms.Form):
    resource_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(validators=[is_email_left_part])
    domain_id = forms.TypedChoiceField(coerce=int)
    whitelist = forms.CharField(label='only e-mails from', required=False)
    redirect_to = forms.EmailField(label='are forwarded to')
    is_enabled = forms.BooleanField(required=False, label='')
    send_test = forms.BooleanField(required=False, label='')

    def __init__(self, handler, *args, **kwargs):
        self.handler = handler
        domains = kwargs.pop('domains_choices', [])

        super(AliasForm, self).__init__(*args, **kwargs)

        self.fields['domain_id'].choices = [(domain.resource_id, domain.name) for domain in domains]
        self.label_suffix = ''
        self.fields['name'].widget.attrs = {
            'placeholder': 'alias name'
        }
        self.fields['whitelist'].widget.attrs = {
            'placeholder': '@website.com'
        }
        self.fields['redirect_to'].widget.attrs = {
            'placeholder': 'your-email@domain.com'
        }

    def send_test_email(self, email):
        subject = "Alias created"
        message = "Your new alias {} is working!".format(email)
        recipient_list = [email, ]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)

    def save(self, request):
        raise NotImplementedError
