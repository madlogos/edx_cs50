from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Username", max_length=128, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Password", max_length=256, required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password_cfm = forms.CharField(
        label="Confirm Password", max_length=256, required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label="First Name", max_length=30, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label="Last Name", max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        label="Email Address", max_length=128, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        filter_result = User.objects.filter(username__exact=username)
        if len(filter_result) > 0:
            raise forms.ValidationError("Your username already exists.")
        return username

    def clean_password_cfm(self):
        pwd1 = self.cleaned_data.get("password")
        pwd2 = self.cleaned_data.get("password_cfm")
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError("Password mismatch. Please enter again.")
        return pwd2


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username", max_length=128, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label="Password", max_length=256, required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        filter_result = User.objects.filter(username__exact=username)
        if not filter_result:
            raise forms.ValidationError("This username does not exist. Please register first.")
        return username
