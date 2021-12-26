from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError

from .models import Service, ServiceOption, ReviewRating


class ServiceCreationForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ['name', 'parent', 'description', 'image']


class ServiceOptionCreationForm(forms.ModelForm):

    class Meta:
        model = ServiceOption
        fields = ['service', 'name', 'summary',
                  'pricing', 'image', 'is_active']


class ReviewRatingForm(forms.ModelForm):

    class Meta:
        model = ReviewRating
        fields = ['service_option', 'subject', 'review', 'rating', ]
        widgets = {
            'rating': forms.RadioSelect()
        }


class SearchForm(forms.Form):
    q = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].label = 'Search For'


class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(
        max_length=500, widget=forms.Textarea()
    )
