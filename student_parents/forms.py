
from django import forms
from django.forms import ModelForm
from .models import (Documents, 
                     Student,
                     ParentDetails,
                     ContactDetails,
                     AdditionalDetails)
from django.forms.widgets import DateInput, Select



class StudentFrom(ModelForm):
    class Meta:
        model = Student
        exclude = ['user', 'create_at', 'student_id']
        widgets = {
            'DOB': DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(StudentFrom, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class DocumentsFrom(ModelForm):
    class Meta:
        model = Documents
        exclude = ['user', 'create_at', 'student_id']

    def __init__(self, *args, **kwargs):
        super(DocumentsFrom, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control pb-4'


class ParentDetailsFrom(ModelForm):
    class Meta:
        model = ParentDetails
        exclude = ['user', 'create_at', 'student_id']
        widgets = {
            'father_dob': DateInput(attrs={'type': 'date'}),
            'mother_dob': DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(ParentDetailsFrom, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ContactDetailsFrom(ModelForm):
    class Meta:
        model = ContactDetails
        exclude = ['user', 'create_at', 'student_id']
        CHOICES = [('1', 'First'), ('2', 'Second')]
        widgets = {
            'state': Select(attrs={'class':'form-select'}),
            'city': Select(attrs={'class':'form-select'}),
            'permanent_state':Select(attrs={'class':'form-control'}),
            'permanent_city':Select(attrs={'class':'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        super(ContactDetailsFrom, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class AdditionalDetailsFrom(ModelForm):
    class Meta:
        model = AdditionalDetails
        exclude = ['user', 'create_at', 'student_id']

    def __init__(self, *args, **kwargs):
        super(AdditionalDetailsFrom, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'