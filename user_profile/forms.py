from django import forms
from django.contrib.auth.models import User
from .models import Profile, Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['title', 'address']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-3 py-2 text-coklat-2 bg-[#F6F6F6] border border-gray-600 rounded-lg border-[#754b0b40]',
            })

class CombinedForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=15, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-3 py-2 text-coklat-2 bg-[#F6F6F6] border border-gray-600 rounded-lg border-[#754b0b40]',
            })
