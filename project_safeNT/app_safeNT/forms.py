from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Patient, CCTVFootage

class RegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'InputStyle',  # Updated class name
                'placeholder': field.label
            })

class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'InputStyle',  # Updated class name
        'placeholder': 'Username'
    }))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={
        'class': 'InputStyle',  # Updated class name
        'placeholder': 'Password'
    }))

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'medical_history', 'assigned_doctor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'InputStyle',  # Updated class name
                'placeholder': field.label
            })

class CCTVForm(forms.ModelForm):
    class Meta:
        model = CCTVFootage
        fields = ['location', 'timestamp', 'video_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'InputStyle',  # Updated class name
                'placeholder': field.label
            })

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, initial='doctor')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role')

class UserModificationForm(UserChangeForm):
    role = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'email', 'role')
