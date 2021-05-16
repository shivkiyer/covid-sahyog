from django import forms

from .models import RequestHelp


class RequestHelpForm(forms.ModelForm):
    display_name = forms.CharField(
                widget=forms.TextInput(attrs={'class': 'form-control'})
            )
    city = forms.CharField(
                widget=forms.TextInput(attrs={'class': 'form-control'})
            )
    twitter_handle = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control'})
            )
    mobile_number = forms.IntegerField(
                error_messages={'invalid': 'Mobile number should only be digits.'},
                widget=forms.TextInput(attrs={'class': 'form-control'})
            )
    email = forms.EmailField(
                required=False,
                widget=forms.EmailInput(attrs={'class': 'form-control'})
            )
    description = forms.CharField(
                widget=forms.Textarea(attrs={'class': 'form-control'})
            )
    address = forms.CharField(
                widget=forms.Textarea(attrs={'class': 'form-control'})
            )
    assistance_url = forms.URLField(
                required=False,
                widget=forms.URLInput(attrs={'class': 'form-control'})
            )
    start_date = forms.DateTimeField(
                required=False,
                widget=forms.DateTimeInput(attrs={'class': 'form-control'})
            )
    end_date = forms.DateTimeField(
                required=False,
                widget=forms.DateTimeInput(attrs={'class': 'form-control'})
            )

    class Meta:
        model = RequestHelp
        fields = [
            'display_name',
            'twitter_handle',
            'mobile_number',
            'email',
            'help_needed',
            'is_help_offered',
            'state',
            'city',
            'description',
            'address',
            'verified',
            'assistance_url',
            'is_disabled'
        ]
