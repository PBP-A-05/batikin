from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_time', 'participants']
        widgets = {
            'booking_time': forms.TimeInput(attrs={'type': 'time'}),
            'participants': forms.NumberInput(attrs={'min': 1, 'value': 1}),
        }
