from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import UserProfile

class StyleMixin:
    """Mixin to add consistent styling to all form fields."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Base classes for all fields
            base_classes = (
                'w-full px-4 py-2 mt-2 border rounded-md '
                'focus:outline-none focus:ring-1 focus:ring-blue-600 '
                'focus:border-blue-600 block'
            )
            
            # Add specific classes based on field type
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = f'{base_classes} resize-none h-32'
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs['class'] = f'{base_classes} tracking-wide'
            else:
                field.widget.attrs['class'] = base_classes
            
            # Add placeholder if not present
            if not field.widget.attrs.get('placeholder'):
                field.widget.attrs['placeholder'] = field.label or field_name.title()

class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form with additional fields."""
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        required=True,
        help_text="Enter your phone number in international format (+999999999)"
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text="Enter your full address"
    )

    # Role selection field
    ROLE_CHOICES = [
        ('CITIZEN', 'Citizen'),  # Default role
        ('POLICE', 'Police'),
        ('DOCTOR', 'Doctor')
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, help_text="Select your role")

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "address", "role", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize help texts
        self.fields['username'].help_text = "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        self.fields['password1'].help_text = "Your password should contain at least 8 characters."
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        
        # Determine the appropriate role
        selected_role = self.cleaned_data["role"]
        
        if commit:
            user.save()  # Save the user instance first
            
            # Assign role based on selection
            if selected_role == 'CITIZEN':
                profile_role = 'CITIZEN'
                intended_role = 'CITIZEN'
            else:
                profile_role = 'PENDING'
                intended_role = selected_role

            # Create or update profile with roles
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'phone_number': self.cleaned_data.get("phone_number"),
                    'address': self.cleaned_data.get("address"),
                    'role': profile_role,          # Role is 'CITIZEN' or 'PENDING'
                    'intended_role': intended_role # Intended role for POLICE or DOCTOR
                }
            )
        return user
    
class CustomAuthenticationForm(StyleMixin, AuthenticationForm):
    """Custom login form with enhanced styling and validation."""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'autocomplete': 'username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'autocomplete': 'current-password',
        })
    )

    error_messages = {
        'invalid_login': "Please enter a correct username and password. Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive. Please contact the administrator.",
    }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return cleaned_data