from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['category', 'description', 'date_started', 'date_completed', 'cert_file']
