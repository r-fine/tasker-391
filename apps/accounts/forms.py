from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import LocalUser, Staff
from apps.services.models import Service


class SignupForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First name'})
    )
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last name'})
    )
    is_staff = forms.BooleanField(required=False)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = self.cleaned_data['is_staff']
        user.save()


class RegisterStaffForm(UserCreationForm):
    class Meta:
        model = LocalUser
        fields = [
            'email', 'first_name', 'last_name',
            'password1', 'password2',
            'is_staff'
        ]

    def __init__(self, *args, **kwargs):
        super(RegisterStaffForm, self).__init__(*args, **kwargs)
        self.fields['email'].help_text = 'e.g. name@example.com'
        self.fields['password1'].help_text = None
        # self.fields['password2'].help_text = None
        self.fields['is_staff'].help_text = None
        self.fields['is_staff'].label = 'Confirm register as a staff'
        # self.fields['is_staff'].required = True


class StaffEditForm(forms.ModelForm):
    # is_active = forms.BooleanField(widget=forms.NullBooleanSelect())
    # department = forms.ModelChoiceField(
    #     queryset=Service.objects.filter(level=0)
    # )

    class Meta:
        model = Staff
        fields = ['department', 'profile_pic', 'phone', 'address', 'is_active']


class LocalUserForm(forms.ModelForm):

    class Meta:
        model = LocalUser
        fields = ['username', 'first_name', 'last_name', 'email']
