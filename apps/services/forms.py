from django import forms

from .models import Service, ServiceOption, ReviewRating


class ServiceCreationForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ['name', 'parent', 'description', 'image']


class ServiceOptionCreationForm(forms.ModelForm):

    class Meta:
        model = ServiceOption
        fields = ['service', 'name', 'summary', 'notes', 'image', 'is_active']


class ReviewRatingForm(forms.ModelForm):

    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']