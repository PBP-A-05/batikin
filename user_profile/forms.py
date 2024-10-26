from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address_line1', 'address_line2', 'profile_picture']
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Apply the same styling as your authentication forms
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-3 py-2 text-coklat-2 bg-[#F6F6F6] border border-gray-600 rounded-lg border-[#754b0b40]',
            })
