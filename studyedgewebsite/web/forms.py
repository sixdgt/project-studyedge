from django import forms
from .models import BookTest, CallbackRequest, CounsellingAppointment

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
            'full_name': forms.TextInput(attrs={'type': 'text', 'class': 'w-full p-3 rounded-lg border dark:border-gray-700 dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-3 rounded-lg border dark:border-gray-700 dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500'}),
            'contact_number': forms.TextInput(attrs={'class': 'w-full p-3 rounded-lg border dark:border-gray-700 dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500'}),
            'preferred_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-3 rounded-lg border dark:border-gray-700 dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500'}),
            'preferred_destination': forms.Select(attrs={'class': 'w-full p-3 rounded-lg border dark:border-gray-700 dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500'}),
            'academic_level': forms.Select(attrs={'class': 'w-full p-3 rounded-lg border dark:border-gray-700 dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500'}),
            'current_academic_level': forms.Select(attrs={'class': 'w-full p-3 rounded-lg border dark:border-gray-700 dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500'}),
            'counselling_mode': forms.Select(attrs={'class': 'w-full p-3 rounded-lg border dark:border-gray-700 dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500'}),
            'address': forms.TextInput(attrs={'type': 'text', 'class': 'w-full p-3 rounded-lg border dark:border-gray-700 dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500'}),
            'preferred_time': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full p-3 rounded-lg border dark:border-gray-700 dark:bg-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500'}),
            'accept_terms': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-blue-600'})
        }