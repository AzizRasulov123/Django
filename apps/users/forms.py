from django import forms


from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))




    class Meta:
        fields = ['username', 'email', 'password1', 'password2']
        model = User
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            })
        }



