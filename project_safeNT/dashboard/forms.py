from django import forms
from .models import Doctor, Patient, Appointment, Incident

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'phone', 'problem', 'medical_history']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time']



class DoctorProfileForm(forms.ModelForm):
    available_time_start = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        label="Available Start Time",
        help_text="Specify the start time for doctor's availability (e.g., 09:00).",
    )
    available_time_end = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        label="Available End Time",
        help_text="Specify the end time for doctor's availability (e.g., 17:00).",
    )

    class Meta:
        model = Doctor
        fields = [
            'name', 'specialization', 'qualification', 'experience_years', 
            'license_number', 'profile_picture', 'bio', 'consultation_fee', 
            'available_days', 'available_time_start', 'available_time_end'
        ]
        widgets = {
            'available_days': forms.TextInput(attrs={'placeholder': 'Mon,Tue,Wed', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'available_days': 'Enter available days as comma-separated values (e.g., "Mon,Tue,Wed").',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("available_time_start")
        end_time = cleaned_data.get("available_time_end")

        if start_time and end_time:
            # Validate that start time is before end time
            if start_time >= end_time:
                self.add_error('available_time_end', "End time must be after start time.")
        return cleaned_data

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['location', 'message']
        widgets = {
            'location': forms.TextInput(attrs={
                'class': 'form-control border border-gray-300 rounded-lg p-3 focus:outline-none focus:border-blue-500',
                'placeholder': 'Enter location'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control border border-gray-300 rounded-lg p-3 focus:outline-none focus:border-blue-500',
                'placeholder': 'Describe the incident',
                'rows': 4
            }),
        }