from django import forms
from django.utils import timezone
from .models import BookTest, CallbackRequest, CounsellingAppointment

# Common CSS class for consistent styling
INPUT_CLASS = 'w-full p-3 rounded-lg border dark:border-gray-700 dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500'
SELECT_CLASS = INPUT_CLASS + ' appearance-none cursor-pointer'
CHECKBOX_CLASS = 'mt-1 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
CALL_BACK_INPUT = 'w-full border border-gray-300 dark:border-gray-700 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white'
BOOK_TEST_INPUT = 'w-full p-3 rounded-lg border dark:border-gray-700 dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500'

# Advanced version with more features
# Single-line class strings (no line breaks)
MODERN_INPUT_VARIANT = 'w-full px-4 py-3.5 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-3 focus:ring-blue-500/30 focus:border-blue-500 transition-all duration-300 ease-out hover:border-blue-400 hover:shadow-sm placeholder:text-transparent text-gray-800 text-base shadow-sm'

MODERN_SELECT_VARIANT = 'w-full px-4 py-3.5 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-3 focus:ring-blue-500/30 focus:border-blue-500 transition-all duration-300 ease-out hover:border-blue-400 hover:shadow-sm appearance-none cursor-pointer text-gray-800 shadow-sm bg-no-repeat bg-[center_right_1rem]'

MODERN_CHECKBOX_VARIANT = 'w-6 h-6 rounded-lg border-2 border-gray-300 checked:bg-gradient-to-r checked:from-blue-600 checked:to-blue-700 checked:border-blue-600 checked:shadow-md focus:ring-3 focus:ring-blue-500/40 focus:ring-offset-1 transition-all duration-300 ease-in-out cursor-pointer appearance-none relative hover:border-blue-400'

class BookTestForm(forms.ModelForm):
    class Meta:
        model = BookTest
        fields = [
            'full_name',
            'email',
            'contact_number',
            'preferred_date',
            'test_type',
            'test_mode',
            'confirmation_status',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'type': 'text',
                'class': MODERN_INPUT_VARIANT,
                'placeholder': ' ',
                'id': 'full-name',
                'required': True,
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': MODERN_INPUT_VARIANT,
                'placeholder': ' ',
                'id': 'email',
                'required': True,
                'autocomplete': 'email',
            }),
            'contact_number': forms.TextInput(attrs={
                'class': MODERN_INPUT_VARIANT,
                'placeholder': ' ',
                'id': 'contact',
                'required': True,
                'autocomplete': 'tel',
            }),
            'preferred_date': forms.DateInput(attrs={
                'type': 'date',
                'class': MODERN_INPUT_VARIANT,
                'id': 'preferred-date',
                'required': True,
            }),
            'test_type': forms.Select(attrs={
                'class': MODERN_SELECT_VARIANT,
                'id': 'test-type',
                'required': True,
            }),
            'test_mode': forms.Select(attrs={
                'class': MODERN_SELECT_VARIANT,
                'id': 'test-mode',
                'required': True,
            }),
            'confirmation_status': forms.CheckboxInput(attrs={
                'class': MODERN_CHECKBOX_VARIANT,
                'id': 'consent',
                'required': True,
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class CallbackRequestForm(forms.ModelForm):
    class Meta:
        model = CallbackRequest
        fields = [
            'full_name',
            'country',
            'contact_number',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'type': 'text', 'class': CALL_BACK_INPUT, 'placeholder': 'Enter your full name'}),
            'country': forms.TextInput(attrs={'type': 'text', 'class': CALL_BACK_INPUT, 'placeholder': 'Enter your country'}),
            'contact_number': forms.TextInput(attrs={'type': 'tel', 'class': CALL_BACK_INPUT, 'placeholder': 'Enter your contact number'}),
        }


class CounsellingAppointmentForm(forms.ModelForm):
    class Meta:
        model = CounsellingAppointment
        fields = "__all__"

    def clean_preferred_date(self):
        date = self.cleaned_data.get('preferred_date')
        if date and date < timezone.now().date():
            raise forms.ValidationError("You cannot select a past date.")
        return date

    def clean_contact_number(self):
        number = self.cleaned_data.get('contact_number')
        if number and not number.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        return number

    def clean_accept_terms(self):
        accepted = self.cleaned_data.get("accept_terms")
        if not accepted:
            raise forms.ValidationError("You must accept the terms.")
        return accepted

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("preferred_date")
        time = cleaned_data.get("preferred_time")

        if date and time:
            if CounsellingAppointment.objects.filter(
                preferred_date=date,
                preferred_time=time
            ).exists():
                raise forms.ValidationError(
                    "This time slot is already booked. Please choose another time."
                )

        return cleaned_data