from django import forms
from django.utils.safestring import mark_safe

class LogInForm(forms.Form):
    handle = forms.CharField(label='Handle')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class SignUpForm(forms.Form):
    username = forms.CharField(label='Username')
    pfp = forms.ImageField(label=mark_safe('<br/>Profile Picture'))
    handle = forms.CharField(label='Handle')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
