from django import forms
from .models import BookTest, CallbackRequest, CounsellingAppointment

# Common CSS class for consistent styling
INPUT_CLASS = 'w-full p-3 rounded-lg border dark:border-gray-700 dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500'
SELECT_CLASS = 'w-full p-3 rounded-lg border dark:border-gray-700 dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500'
CHECKBOX_CLASS = 'mt-1 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
CALL_BACK_INPUT = 'w-full border border-gray-300 dark:border-gray-700 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white'
BOOK_TEST_INPUT = 'w-full p-3 rounded-lg border dark:border-gray-700 dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500'

# Advanced version with more features
MODERN_INPUT_VARIANT = {
    'default': """
        w-full px-4 py-3.5 bg-white border border-gray-300 rounded-xl 
        focus:outline-none focus:ring-3 focus:ring-blue-500/30 focus:border-blue-500 
        transition-all duration-300 ease-out hover:border-blue-400 hover:shadow-sm
        placeholder:text-transparent text-gray-800 text-base
        shadow-sm
    """,
    
    'focus': """
        w-full px-4 py-3.5 bg-white border-2 border-blue-500 rounded-xl 
        ring-3 ring-blue-500/20 shadow-md
        placeholder:text-transparent text-gray-800 text-base
        transition-all duration-300 ease-out
    """,
}

MODERN_SELECT_VARIANT = """
    w-full px-4 py-3.5 bg-white border border-gray-300 rounded-xl 
    focus:outline-none focus:ring-3 focus:ring-blue-500/30 focus:border-blue-500 
    transition-all duration-300 ease-out hover:border-blue-400 hover:shadow-sm
    appearance-none bg-gradient-to-r from-blue-50/50 to-white
    bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMCAyMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNNiA4TDEwIDEyTDE0IDgiIHN0cm9rZT0iIzM3NDE1MSIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPjwvc3ZnPg==')]
    bg-no-repeat bg-[center_right_1rem] bg-[length:20px_20px]
    cursor-pointer text-gray-800 shadow-sm
"""

MODERN_CHECKBOX_VARIANT = """
    w-6 h-6 rounded-lg border-2 border-gray-300 
    checked:bg-gradient-to-r checked:from-blue-600 checked:to-blue-700 
    checked:border-blue-600 checked:shadow-md
    focus:ring-3 focus:ring-blue-500/40 focus:ring-offset-1 
    transition-all duration-300 ease-in-out cursor-pointer
    appearance-none relative
    checked:before:absolute checked:before:content-["✓"] 
    checked:before:text-white checked:before:text-base 
    checked:before:font-bold checked:before:left-1/2 
    checked:before:top-1/2 checked:before:-translate-x-1/2 
    checked:before:-translate-y-1/2
    hover:border-blue-400
"""

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
                'class': MODERN_INPUT_VARIANT['default'],
                'placeholder': ' ',
                'id': 'full-name',
                'required': True,
                'data-floating': 'true',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': MODERN_INPUT_VARIANT['default'],
                'placeholder': ' ',
                'id': 'email',
                'required': True,
                'data-floating': 'true',
                'autocomplete': 'email',
            }),
            'contact_number': forms.TextInput(attrs={
                'class': MODERN_INPUT_VARIANT['default'],
                'placeholder': ' ',
                'id': 'contact',
                'required': True,
                'data-floating': 'true',
                'autocomplete': 'tel',
            }),
            'preferred_date': forms.DateInput(attrs={
                'type': 'date',
                'class': MODERN_INPUT_VARIANT['default'] + " date-picker-icon",
                'id': 'preferred-date',
                'required': True,
                'data-floating': 'true',
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
        
        # Add custom attributes for JavaScript interactions
        for field_name, field in self.fields.items():
            if field_name != 'confirmation_status':
                field.widget.attrs.update({
                    'class': field.widget.attrs.get('class', '') + ' form-input-peer',
                })
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
        fields = [
            'full_name',
            'email',
            'address',
            'contact_number',
            'preferred_date',
            'preferred_time',
            'preferred_destination',
            'intended_academic_level',
            'current_academic_level',
            'counselling_mode',
            'accept_terms',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'type': 'text', 'class': INPUT_CLASS, 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Enter your email'}),
            'contact_number': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Enter your contact number'}),
            'preferred_date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASS}),
            'preferred_destination': forms.Select(attrs={'class': SELECT_CLASS}),
            'intended_academic_level': forms.Select(attrs={'class': SELECT_CLASS}),
            'current_academic_level': forms.Select(attrs={'class': SELECT_CLASS}),
            'counselling_mode': forms.Select(attrs={'class': SELECT_CLASS}),
            'address': forms.TextInput(attrs={'type': 'text', 'class': INPUT_CLASS, 'placeholder': 'Enter your address'}),
            'preferred_time': forms.TimeInput(attrs={'type': 'time', 'class': INPUT_CLASS}),
            'accept_terms': forms.CheckboxInput(attrs={'class': CHECKBOX_CLASS}),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'contact_number': 'Contact Number',
            'address': 'Address',
            'preferred_date': 'Preferred Date',
            'preferred_time': 'Preferred Time',
            'preferred_destination': 'Study Destination',
            'intended_academic_level': 'Intended Academic Level',
            'current_academic_level': 'Current Academic Level',
            'counselling_mode': 'Counselling Mode',
            'accept_terms': 'I accept the terms and conditions',
        }