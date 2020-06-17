from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

username_validator = UnicodeUsernameValidator()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, min_length=4, required=True, help_text='Required: First Name',
                                widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=False,min_length=4,widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length = 50, help_text = 'Required. Inform a valid email address.',
                             widget = (forms.TextInput(attrs={'placeholder': 'Email'})))
    password1 = forms.CharField(label = _('Password'),
                                help_text = password_validation.password_validators_help_text_html(), 
                                widget = forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label =_('Password Confirmation'),
                                help_text = password_validation.password_validators_help_text_html(), 
                                widget = forms.PasswordInput(attrs={'placeholder': 'Password'}))
    username = forms.CharField(
        label=_('Username'),
        max_length=150,
        validators=[username_validator],
        error_messages={'unique': _("A user with that username already exists.")},
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        )
    Bio = forms.CharField(max_length = 200,label=_('Bio'),required = False,
                                widget=forms.TextInput(attrs={'placeholder': 'Bio'}),
                                help_text=_('Tell us something about yourself'))
    

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email','Bio')