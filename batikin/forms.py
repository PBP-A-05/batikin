from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-3 py-2 text-coklat-2 bg-[#F6F6F6] border border-gray-600 rounded-lg border-[#754b0b40]',
            'placeholder': 'Username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-3 py-2 text-coklat-2 bg-[#F6F6F6] border border-gray-600 rounded-lg border-[#754b0b40]',
            'placeholder': 'Password',
        })


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-3 py-2 text-coklat-2 bg-[#F6F6F6] border border-gray-600 rounded-lg border-[#754b0b40]',
            'placeholder': 'Username',
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'w-full px-3 py-2 text-coklat-2 bg-[#F6F6F6] border border-gray-600 rounded-lg border-[#754b0b40]',
            'placeholder': 'First Name',
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'w-full px-3 py-2 text-coklat-2 bg-[#F6F6F6] border border-gray-600 rounded-lg border-[#754b0b40]',
            'placeholder': 'Last Name',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-3 py-2 text-coklat-2 bg-[#F6F6F6] border border-gray-600 rounded-lg border-[#754b0b40]',
            'placeholder': 'Password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-3 py-2 text-coklat-2 bg-[#F6F6F6] border border-gray-600 rounded-lg border-[#754b0b40] border-[#754b0b40]',
            'placeholder': 'Confirm Password',
        })


