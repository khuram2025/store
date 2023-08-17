from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['name', 'mobile_number', 'password1', 'password2']

class LoginForm(forms.Form):
    mobile_number = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)
from django import forms
from .models import UserProfile
class UserProfileForm(forms.ModelForm):
    mobile_number = forms.CharField(max_length=15, required=True)  # Make it required as it exists during signup
    name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=False)  # Make email optional

    class Meta:
        model = UserProfile
        fields = ['mobile_number', 'name', 'profile_image', 'cover_image', 'email', 'location', 'city']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['mobile_number'].initial = self.instance.user.mobile_number
            self.fields['name'].initial = self.instance.user.name
        self.fields['profile_image'].required = False
        self.fields['cover_image'].required = False

    def save(self, *args, **kwargs):
        profile = super().save(*args, **kwargs)
        profile.user.mobile_number = self.cleaned_data['mobile_number']
        profile.user.name = self.cleaned_data['name']
        profile.user.save()
        return profile


class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', "Password and password confirmation must match.")