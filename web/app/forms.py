from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=30)
    university = forms.CharField(max_length=60)
    has_meal_plan = forms.BooleanField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords must match.')


class ListingForm(forms.Form):
    title = forms.CharField(max_length=80)
    description = forms.TextField(max_length=1000)
    listing_type = forms.CharField(
        choices=[('S', 'Swipe'), ('M', 'Meal Exchange'), ('I', 'Item')],
        widgets=forms.RadioSelect(),
    )
    num_swipes = forms.IntegerField(min_value=1, max_value=200)
