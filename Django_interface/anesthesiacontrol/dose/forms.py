from django import forms

class PatientDetailsForm(forms.Form):
    name = forms.CharField(label="Patient Name", max_length=100)
    age = forms.IntegerField(label="Patient Age")