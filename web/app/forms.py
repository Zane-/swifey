from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

import requests

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'login'
        self.helper.form_class = 'from-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'
        self.helper.form_method = 'post'
        self.helper.form_action = 'login'
        self.helper.add_input(Submit('submit', 'Login'))

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=30)
    university = forms.CharField(max_length=60)
    has_meal_plan = forms.BooleanField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'signup'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'signup'
        self.helper.add_input(Submit('submit', 'Sign up'))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords must match.')

        email = cleaned_data.get('email')
        data = {'email': email}
        req = requests.post('http://exp-api:8000/api/validate_email/', data=data)
        if req.status_code != 200:
            raise forms.ValidationError('Email already in use.')


class ListingForm(forms.Form):
    title = forms.CharField(max_length=80)
    description = forms.CharField(max_length=1000, widget=forms.Textarea)
    listing_type = forms.ChoiceField(
        choices=(('S', 'Swipe'), ('M', 'Meal Exchange'), ('I', 'Item')),
        widget=forms.RadioSelect(),
    )
    num_swipes = forms.IntegerField(min_value=1, max_value=200)

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'create_listing'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'create_listing'
        self.helper.add_input(Submit('submit', 'Create'))
