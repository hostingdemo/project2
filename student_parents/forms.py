
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Div, Layout, Row, Field, Submit
from django.forms import ModelForm
from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms.widgets import DateInput, Select

from .models import (Child, CommonForm)


## 
# child form
##
class ChildForm(BSModalModelForm):
    class Meta:
        model = Child
        exclude = ['user']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(ChildForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'


## 
# child info form
##
class CommonFormForm(ModelForm):
    class Meta:
        model = CommonForm
        exclude = ['student_id', 'child' ]
        widgets = {
            'fathers_dob': DateInput(attrs={'type': 'date'}),
            'mothers_dob': DateInput(attrs={'type': 'date'}),
            'state': Select(),
            'city': Select(attrs={'disabled': True}),
            'permanent_state': Select(),
            'permanent_city': Select(attrs={'disabled': True}),
        }

    def __init__(self, *args, **kwargs):
        super(CommonFormForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'

        self.helper = FormHelper()
        self.helper.form_class = "needs-validation"
        self.helper.form_id = 'common-form'
        self.helper.attrs = {"novalidate": ''}
        self.helper.layout = Layout(
            ## 
            # Child Details
            ##
            HTML('<div style="overflow: hidden;" class="card shadow-sm border-0 mt-3 mb-5">'),
            HTML('<div class="card-header">Child Details</div>'),
            HTML('<div class="card-body">'),
            Row(
                Column(Field('blood_group', wrapper_class='mr-2'), css_class='col-12 col-md-2'),
                Column(Field('religion', wrapper_class='mx-2'), css_class='col-12 col-md-4'),
                Column(Field('category', wrapper_class='mx-2'), css_class='col-12 col-md-4'),
                Column(Field('minority', wrapper_class='ml-2'), css_class='col-12 col-md-2'),
                css_class='row',
            ), 
            Row(
                Column(Field('aadhar_no', wrapper_class='mr-2'), css_class='col-12 col-md-6'),
                Column(Field('admission_number', wrapper_class='ml-2'), css_class='col-12 col-md-6'),
            ),
            Row(
                Field('single_child', wrapper_class='mr-2 mr-md-3'),
                Field('adopted_child', wrapper_class='mr-2 mr-md-3'),
                Field('orphan_child', wrapper_class='mr-2 mr-md-3'),
                Field('child_with_needs', wrapper_class='mr-2 mr-md-3'),
                css_class='ml-2'
            ),
            HTML('</div>'),
            HTML('</div>'),

            ## 
            # Contact Details
            ##
            HTML('<div style="overflow: hidden;" class="card shadow-sm border-0 mt-3 mb-5">'),
            HTML('<div class="card-header">Contact Details</div>'),
            HTML('<div class="card-body">'),
            Div(
                Div(
                    Row(
                        Column(Field('current_address_line_1', wrapper_class='mr-2'), css_class='col-12 col-md-6'),
                        Column(Field('current_address_line_2', wrapper_class='ml-2'), css_class='col-12 col-md-6'),
                        Column(Field('state'), css_class='col-12 col-md-4'),
                        Column(Field('city'), css_class='col-12 col-md-4'),
                        Column(Field('pincode'), css_class='col-12 col-md-4'),
                    ),
                    css_class='border rounded p-3'
                ),
                Div(
                    Row(
                        Column(Field('permanent_address_line_1', wrapper_class='mr-2'), css_class='col-12 col-md-6'),
                        Column(Field('permanent_address_line_2', wrapper_class='ml-2'), css_class='col-12 col-md-6'),
                        Column(Field('permanent_state'), css_class='col-12 col-md-4'),
                        Column(Field('permanent_city'), css_class='col-12 col-md-4'),
                        Column(Field('permanent_pincode'), css_class='col-12 col-md-4'),
                    ),
                    css_class='border rounded p-3'
                ),
                css_class='address'
            ), 
            HTML('</div>'),
            HTML('</div>'),

            ## 
            # Parents/ Gardian Details
            ##
            HTML('<div style="overflow: hidden;" class="card shadow-sm border-0 mt-3 mb-5">'),
            HTML('<div class="card-header">Parents/ Gardian Details</div>'),
            HTML('<div class="card-body">'),
            Row(
                Column(Field('fathers_name', wrapper_class='mr-2'), css_class='col-12 col-md-4'),
                Column(Field('fathers_dob', wrapper_class='mx-2'), css_class='col-12 col-md-4'),
                Column(Field('fathers_qualification', wrapper_class='ml-2'), css_class='col-12 col-md-4'),
                
                Column(Field('mothers_name', wrapper_class='mr-2'), css_class='col-12 col-md-4'),
                Column(Field('mothers_dob', wrapper_class='mx-2'), css_class='col-12 col-md-4'),
                Column(Field('mothers_qualification', wrapper_class='ml-2'), css_class='col-12 col-md-4'),
                
                Column(Field('email', wrapper_class='mr-2'), css_class='col-12 col-md-4'),
                Column(Field('phone_no', wrapper_class='mx-2'), css_class='col-12 col-md-4'),
                Column(Field('alternate_phone_no', wrapper_class='ml-2'), css_class='col-12 col-md-4'),

                Column(Field('family_annual_income'), css_class='col-12'),
            ),
            HTML('</div>'),
            HTML('</div>'),

            ## 
            # Additional Details
            ##
            HTML('<div style="overflow: hidden;" class="card shadow-sm border-0 mt-3 mb-5">'),
            HTML('<div class="card-header">Additional Details</div>'),
            HTML('<div class="card-body">'),
            Row(
                Column(Field('privious_school', wrapper_class='mr-2'), css_class='col-12'),
                Column(Field('transfer_certificate_no', wrapper_class='mx-2'), css_class='col-12 col-md-3'),
                Column(Field('route_code', wrapper_class='ml-2'), css_class='col-12 col-md-3'),
                Column(Field('shift', wrapper_class='mr-2'), css_class='col-12 col-md-3'),
                Column(Field('stoppage_name', wrapper_class='mx-2'), css_class='col-12 col-md-3'),
            ),
            HTML('</div>'),
            HTML('</div>'),

            ## 
            # Documents Details
            ##
            HTML('<div style="overflow: hidden;" class="card shadow-sm border-0 mt-3 mb-5">'),
            HTML('<div class="card-header">Documents Details</div>'),
            HTML('<div class="card-body">'),
            HTML('<table>'),
            Div(
                Field('photo', wrapper_class='m-0'),
                Field('id_proof', wrapper_class='m-0'),
                Field('caste_certificate', wrapper_class='m-0'),
                Field('domicile', wrapper_class='m-0'),
                Field('transfer_certificate', wrapper_class='m-0'),
                Field('character_certificate', wrapper_class='m-0'),
            ),
            HTML('</table>'),
            HTML('</div>'),
            HTML('</div>'),

            HTML('<div class="text-center">'),
            Submit('submit', 'Submit'),
            HTML('</div>'),
        )