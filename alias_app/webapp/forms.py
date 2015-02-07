from django import forms
from alias_app.webapp.models import HostingService


class SetupForm(forms.Form):
    hosting_service = forms.ModelChoiceField(
        queryset=HostingService.objects.all(),
        empty_label="Choose your hosting service"
    )
    api_key = forms.CharField(max_length=200)
