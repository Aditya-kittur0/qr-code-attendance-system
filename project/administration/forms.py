from django import forms
from .models import Student,Session

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'roll_number']

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session  # The model the form is tied to
        fields = ['title','duration_seconds']
    num_sessions = forms.IntegerField(min_value=1, label="Number of Sessions")
    